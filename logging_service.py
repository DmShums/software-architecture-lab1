import uuid
from fastapi import FastAPI
from pydantic import BaseModel
import hazelcast
import os

from consul_service import (
    register_service,
    deregister_service,
    get_kv,
)


CONSUL_HOST      = "localhost"
SERVICE_NAME     = "logging-service"
SERVICE_PORT     = int(os.getenv("LOGGING_PORT", 8002))
SERVICE_ID       = f"{SERVICE_NAME}-{uuid.uuid4()}"

KV_HZ_MEMBERS    = "config/hazelcast/members"
KV_HZ_CLUSTER    = "config/hazelcast/cluster"


app = FastAPI(title="Logging Service")

@app.on_event("startup")
async def on_startup():
    register_service(CONSUL_HOST, SERVICE_NAME, SERVICE_ID, SERVICE_PORT)
    members_csv = get_kv(CONSUL_HOST, KV_HZ_MEMBERS)
    cluster_name = get_kv(CONSUL_HOST, KV_HZ_CLUSTER)
    members = [m.strip() for m in members_csv.split(",") if m.strip()]

    app.state.hz = hazelcast.HazelcastClient(
        cluster_members=members,
        cluster_name=cluster_name
    )
    app.state.map = app.state.hz.get_map("hdmap").blocking()


@app.on_event("shutdown")
async def on_shutdown():
    deregister_service(CONSUL_HOST, SERVICE_ID)
    await app.state.hz.shutdown()


@app.get("/health")
async def health_check():
    return {"status": "UP"}


class RequestModel(BaseModel):
    id: str
    text: str


@app.post("/logging-service")
async def post_request(data: RequestModel):
    app.state.map.put(data.id, data.text)
    return {"message": "Logged successfully"}


@app.get("/logging-service")
async def get_request():
    messages = list(app.state.map.values())
    return {"messages": messages}
