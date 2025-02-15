"""gets POST/GET requests from client"""

from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import uvicorn
import requests

facade_service = FastAPI()

class RequestModel(BaseModel):
    text: str

class FacadeController:
    """Facade controller class"""
    logging_service_url = "http://localhost:8001/logging-service"
    messages_service_url = "http://localhost:8002/message"

    @facade_service.post("/facade-service")
    def post_request(data: RequestModel):
        new_uuid = str(uuid.uuid4())
        message = {"id": new_uuid, "text": data.text}

        requests.post(FacadeController.logging_service_url, json=message)

        return message

    @facade_service.get("/facade-service")
    def get_request():
        logging_response = requests.get(FacadeController.logging_service_url)
        message_response = requests.get(FacadeController.messages_service_url)

        logged_messages = logging_response.json()
        static_message = message_response.json()["message"]

        return {"logged_messages": list(logged_messages), "message": static_message}
