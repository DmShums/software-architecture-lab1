import grpc
from concurrent import futures
from generated import services_pb2, services_pb2_grpc

class MessageServicer(services_pb2_grpc.MessageServiceServicer):
    def GetMessage(self, request, context):
        return services_pb2.MessageResponse(message="Hello from gRPC!")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    services_pb2_grpc.add_MessageServiceServicer_to_server(MessageServicer(), server)
    server.add_insecure_port('[::]:8002')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
