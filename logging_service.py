"""Stores all messages it receives in memory and can return them."""

from fastapi import FastAPI
from pydantic import BaseModel

logging_service = FastAPI()

class RequestModel(BaseModel):
    id: str
    text: str

class LoggingController:
    """Logging controller class"""
    messages = {}

    @logging_service.post("/logging-service")
    def post_request(data: RequestModel):
        LoggingController.messages[data.id] = data.text
        print(f"Received message: {data.text}")
        return {"message": "Logged successfully"}

    @logging_service.get("/logging-service")
    def get_request():
        return list(LoggingController.messages.values())
