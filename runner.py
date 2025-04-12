import uvicorn
import multiprocessing
import os
import hazelcast

from facade_service import facade_service
from logging_service import logging_service
from messages_service import messages_service

FACADE_PORT = 8000
MESSAGES_PORT1 = 8001
MESSAGES_PORT2 = 8005
LOGGING_PORT1 = 8002
LOGGING_PORT2 = 8003
LOGGING_PORT3 = 8004

def run_facade_service():
    uvicorn.run(facade_service, host="0.0.0.0", port=FACADE_PORT)

def run_logging_service(port):
    uvicorn.run(logging_service, host="0.0.0.0", port=port)

def run_messages_service(port):
    uvicorn.run(messages_service, host="0.0.0.0", port=port)

if __name__ == "__main__":
    process_facade = multiprocessing.Process(target=run_facade_service)
    process_messages1 = multiprocessing.Process(target=run_messages_service, args=(MESSAGES_PORT1,))
    process_messages2 = multiprocessing.Process(target=run_messages_service, args=(MESSAGES_PORT2,))
    process_logging1 = multiprocessing.Process(target=run_logging_service, args=(LOGGING_PORT1,))
    process_logging2 = multiprocessing.Process(target=run_logging_service, args=(LOGGING_PORT2,))
    process_logging3 = multiprocessing.Process(target=run_logging_service, args=(LOGGING_PORT3,))

    processes = [
        process_facade,
        process_messages1,
        process_messages2,
        process_logging1,
        process_logging2,
        process_logging3
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()
