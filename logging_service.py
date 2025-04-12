from fastapi import FastAPI
from pydantic import BaseModel
import hazelcast
import os

logging_service = FastAPI()

# Hazelcast client configuration
hazelcast_client = hazelcast.HazelcastClient(
    cluster_members=["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"],
    cluster_name="dev"
)
messages_map = hazelcast_client.get_map("hdmap").blocking()

class RequestModel(BaseModel):
    id: str
    text: str

class LoggingController:
    """Logging controller class"""

    @logging_service.post("/logging-service")
    async def post_request(data: RequestModel):
        messages_map.put(data.id, data.text)
        print(f"Received message: {data.text}")
        return {"message": "Logged successfully"}

    @logging_service.get("/logging-service")
    async def get_request():
        messages_list = list(messages_map.values())
        return {"messages": messages_list}