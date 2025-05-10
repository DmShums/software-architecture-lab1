# logging_service.py
import grpc
from concurrent import futures
from generated import services_pb2, services_pb2_grpc

class LoggingServicer(services_pb2_grpc.LoggingServiceServicer):
    def __init__(self):
        self._messages = {}

    def Log(self, request, context):
        if request.id in self._messages:
            print(f"[logging] Duplicate received, id={request.id}; skipping.")
        else:
            self._messages[request.id] = request.text
            print(f"[logging] Received new message: {request.text!r} (id={request.id})")
        return services_pb2.Empty()

    def GetLogs(self, request, context):
        entries = [
            services_pb2.LogEntry(id=k, text=v)
            for k, v in self._messages.items()
        ]
        return services_pb2.GetLogsResponse(entries=entries)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_LoggingServiceServicer_to_server(LoggingServicer(), server)
    server.add_insecure_port('[::]:8001')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
