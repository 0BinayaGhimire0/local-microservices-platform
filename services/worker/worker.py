from prometheus_client import Counter, start_http_server
from redis import Redis
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
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

TASKS_PROCESSED = Counter(
    "worker_tasks_processed_total",
    "Total number of tasks processed by the worker service",
)

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(
    endpoint="http://jaeger:4317",
    insecure=True,
)

span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

def process_task(task):
    with tracer.start_as_current_span("process_task"):
        logger.info("Processing task", extra={"task_id": task["id"], "message": task["message"]})
        time.sleep(2)
        TASKS_PROCESSED.inc()
        logger.info("Completed task", extra={"task_id": task["id"]})


def main():
    start_http_server(8000)
    logger.info("Worker metrics server started on port 8000")
    logger.info("Worker service started. Waiting for tasks...")

    while True:
        _, task_data = redis_client.brpop("task_queue")
        task = json.loads(task_data)
        process_task(task)


if __name__ == "__main__":
    main()