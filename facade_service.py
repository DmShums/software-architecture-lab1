import uuid
import random
import asyncio

import httpx
from fastapi import FastAPI
from pydantic import BaseModel
from confluent_kafka import Producer

from consul_service import (
    register_service,
    deregister_service,
    discover_service,
    get_kv,
)

CONSUL_HOST     = "localhost"
SERVICE_NAME    = "facade-service"
SERVICE_PORT    = 8000
SERVICE_ID      = f"{SERVICE_NAME}-{uuid.uuid4()}"

KV_KAFKA_BOOT   = "config/kafka/bootstrap"
KV_MQ_QUEUE     = "config/mq/queue_name"

app = FastAPI(title="Facade Service")

@app.on_event("startup")
async def on_startup():
    register_service(CONSUL_HOST, SERVICE_NAME, SERVICE_ID, SERVICE_PORT)

    bootstrap = get_kv(CONSUL_HOST, KV_KAFKA_BOOT)
    print(f"[DEBUG] Kafka bootstrap.servers = {bootstrap!r}")
    app.state.producer = Producer({"bootstrap.servers": bootstrap})

@app.on_event("shutdown")
async def on_shutdown():
    deregister_service(CONSUL_HOST, SERVICE_ID)
    app.state.producer.flush(10.0)

class RequestModel(BaseModel):
    text: str

def build_service_urls(service_name: str, path: str) -> list[str]:
    """
    Query Consul for all healthy instances of `service_name`
    and build full HTTP URLs including the given path.
    """
    instances = discover_service(CONSUL_HOST, service_name)
    urls = []
    for inst in instances:
        host = inst.get("ServiceAddress") or inst.get("Address")
        port = inst["ServicePort"]
        urls.append(f"http://{host}:{port}{path}")
    return urls


@app.post("/facade-service")
async def post_request(payload: RequestModel):
    msg_id = str(uuid.uuid4())
    try:
        app.state.producer.produce(
            topic="messages",
            key=msg_id,
            value=payload.text.encode(),
        )
        app.state.producer.flush()
    except Exception as e:
        return {"error": "Failed to send to Kafka", "details": str(e)}

    logging_urls = build_service_urls("logging-service", "/logging-service")
    random.shuffle(logging_urls)

    async with httpx.AsyncClient() as client:
        for url in logging_urls:
            try:
                r = await client.post(url, json={"id": msg_id, "text": payload.text})
                r.raise_for_status()
                return {"status": "Message logged", "message_id": msg_id}
            except Exception:
                await asyncio.sleep(0.2)
    return {"error": "All logging-service instances unavailable."}


@app.get("/facade-service")
async def get_combined_messages():
    combined = {"logging": [], "messages": []}

    logging_urls = build_service_urls("logging-service", "/logging-service")
    random.shuffle(logging_urls)
    async with httpx.AsyncClient() as client:
        for url in logging_urls:
            try:
                r = await client.get(url)
                r.raise_for_status()
                combined["logging"] = r.json().get("messages", [])
                break
            except Exception:
                await asyncio.sleep(0.2)

    msg_urls = build_service_urls("messages-service", "/messages")
    random.shuffle(msg_urls)
    async with httpx.AsyncClient() as client:
        for url in msg_urls:
            try:
                r = await client.get(url)
                r.raise_for_status()
                combined["messages"] = r.json().get("messages", [])
                break
            except Exception:
                await asyncio.sleep(0.2)

    if not (combined["logging"] or combined["messages"]):
        return {"error": "All downstream services unavailable."}
    return combined