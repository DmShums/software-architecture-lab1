from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import httpx
import random
import asyncio
from confluent_kafka import Producer

facade_service = FastAPI()

producer_config = {"bootstrap.servers": "localhost:9092,localhost:9093,localhost:9094"}

producer = Producer(producer_config)

class RequestModel(BaseModel):
    text: str

class FacadeController:
    """Facade controller class"""
    logging_service_urls = [
        "http://127.0.0.1:8002/logging-service",
        "http://127.0.0.1:8003/logging-service",
        "http://127.0.0.1:8004/logging-service"
    ]

    messages_service_urls = [
        "http://127.0.0.1:8001/messages",
        "http://127.0.0.1:8005/messages"
    ]

    @facade_service.post("/facade-service")
    async def post_request(data: RequestModel):
        new_uuid = str(uuid.uuid4())
        message = {"id": new_uuid, "text": data.text}

        try:
            producer.produce(
                topic="messages",
                key=new_uuid,
                value=data.text.encode("utf-8")
            )
            producer.flush() 
            print(f"Produced message with ID {new_uuid} to Kafka.")
        except Exception as e:
            print(f"Failed to send message to Kafka: {e}")
            return {"error": "Failed to send message to Kafka"}

        # Randomly try one of the logging services
        shuffled_services = random.sample(FacadeController.logging_service_urls,
                                          len(FacadeController.logging_service_urls))
        
        async with httpx.AsyncClient() as client:
            for selected_service in shuffled_services:
                try:
                    response = await client.post(selected_service, json=message)
                    response.raise_for_status()
                    return {"status": "Message logged", "message_id": new_uuid}
                except httpx.RequestError as e:
                    print(f"Request to {selected_service} failed: {e}")
                    await asyncio.sleep(1)

        return {"error": "All logging services are unavailable."}

    @facade_service.get("/facade-service")
    async def get_combined_messages():
        combined_response = {"logging_messages": [], "messages_service_messages": []}
        
        shuffled_logging = random.sample(FacadeController.logging_service_urls,
                                         len(FacadeController.logging_service_urls))
        async with httpx.AsyncClient() as client:
            for url in shuffled_logging:
                try:
                    resp = await client.get(url)
                    resp.raise_for_status()
                    combined_response["logging_messages"] = resp.json().get("messages", [])
                    break
                except httpx.RequestError as e:
                    print(f"Request to logging service {url} failed: {e}")
                    await asyncio.sleep(1)
            

            shuffled_messages = random.sample(FacadeController.messages_service_urls,
                                              len(FacadeController.messages_service_urls))
            for url in shuffled_messages:
                try:
                    resp = await client.get(url)
                    resp.raise_for_status()
                    combined_response["messages_service_messages"] = resp.json().get("messages", [])
                    break
                except httpx.RequestError as e:
                    print(f"Request to messages service {url} failed: {e}")
                    await asyncio.sleep(1)
                    
        if not combined_response["logging_messages"] and not combined_response["messages_service_messages"]:
            return {"error": "All services are unavailable."}
        
        return combined_response
