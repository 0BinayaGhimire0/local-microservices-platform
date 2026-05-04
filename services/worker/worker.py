from redis import Redis
import os
import json
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker-service")

redis_client = Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True,
)


def process_task(task):
    print(f"Processing task: {task['id']}")
    print(f"Message: {task['message']}")
    time.sleep(2)
    print(f"Completed task: {task['id']}")
    logger.info("Processing task", extra={"task_id": task["id"], "message": task["message"]})
    time.sleep(2)
    logger.info("Completed task", extra={"task_id": task["id"]})


def main():
    print("Worker service started. Waiting for tasks...")

    while True:
        _, task_data = redis_client.brpop("task_queue")
        task = json.loads(task_data)
        process_task(task)


if __name__ == "__main__":
    main()