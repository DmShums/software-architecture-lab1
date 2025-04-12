import fastapi
from confluent_kafka import Consumer
from typing import List
import multiprocessing

messages_service = fastapi.FastAPI()


messages: List[str] = []

def consume_messages(group_id):
    config = {
        "bootstrap.servers": "localhost:9092,localhost:9093,localhost:9094",
        "group.id": group_id,
        "auto.offset.reset": "earliest"
    }
    consumer = Consumer(config)
    consumer.subscribe(["messages"])

    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"[ERROR] {msg.error()}")
            continue
        decoded = msg.value().decode("utf-8")
        print(f"[Kafka] {decoded}")
        messages.append(decoded)

# Expose an endpoint that returns all messages from Kafka
@messages_service.get("/messages")
def get_messages():
    return {"messages": messages}

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.set_start_method("spawn", force=True)
    group_id = "message-consumer-group"
    consumer_process = multiprocessing.Process(target=consume_messages, args=(group_id,))
    consumer_process.daemon = True
    consumer_process.start()
