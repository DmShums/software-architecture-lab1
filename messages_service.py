"""returns static message"""

import fastapi

messages_service = fastapi.FastAPI()

@messages_service.get("/message")
def send_message():
    return {"message": "not implemented yet"}
