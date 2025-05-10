# facade_service.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import grpc
from generated import services_pb2, services_pb2_grpc
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

facade_service = FastAPI()

_logging_channel = grpc.insecure_channel('localhost:8001')
_logging_stub   = services_pb2_grpc.LoggingServiceStub(_logging_channel)
_message_channel = grpc.insecure_channel('localhost:8002')
_message_stub   = services_pb2_grpc.MessageServiceStub(_message_channel)

class RequestModel(BaseModel):
    text: str

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=4),
    retry=retry_if_exception_type(grpc.RpcError),
    reraise=True
)
def log_with_retry(log_req: services_pb2.LogRequest):
    attempt = log_with_retry.retry.statistics.get('attempt_number', 1)
    print(f"[facade] Log attempt #{attempt} …")
    return _logging_stub.Log(log_req)

@facade_service.post("/facade-service")
def post_request(data: RequestModel):
    new_id = str(uuid.uuid4())
    log_req = services_pb2.LogRequest(id=new_id, text=data.text)

    try:
        log_with_retry(log_req)
    except grpc.RpcError as e:
        # all retries failed
        raise HTTPException(status_code=503, detail="Logging service unavailable")

    return {"id": new_id, "text": data.text}

@facade_service.get("/facade-service")
def get_request():
    logs_resp = _logging_stub.GetLogs(services_pb2.GetLogsRequest())
    logged = [{"id": e.id, "text": e.text} for e in logs_resp.entries]
    msg_resp = _message_stub.GetMessage(services_pb2.Empty())
    return {"logged_messages": logged, "message": msg_resp.message}
