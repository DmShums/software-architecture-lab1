import os
import multiprocessing
import uvicorn

from facade_service import app as facade_app
from logging_service import app as logging_app
from messages_service import app as messages_app

FACADE_PORT   = 8000
MESSAGES_PORTS = [8001, 8005]
LOGGING_PORTS = [8002, 8003, 8004]


def run_facade_service():
    """Runs the Facade Service on its designated port."""
    uvicorn.run(facade_app, host="0.0.0.0", port=FACADE_PORT)


def run_logging_service(port: int):
    os.environ["LOGGING_PORT"] = str(port)
    uvicorn.run(logging_app, host="0.0.0.0", port=port)


def run_messages_service(port: int):
    os.environ["MESSAGES_PORT"] = str(port)
    uvicorn.run(messages_app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    processes = []

    processes.append(
        multiprocessing.Process(target=run_facade_service)
    )

    for port in MESSAGES_PORTS:
        processes.append(
            multiprocessing.Process(
                target=run_messages_service,
                args=(port,),
            )
        )

    for port in LOGGING_PORTS:
        processes.append(
            multiprocessing.Process(
                target=run_logging_service,
                args=(port,),
            )
        )

    for p in processes:
        p.start()

    for p in processes:
        p.join()