from flask import Flask, jsonify, request, Response
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from redis import Redis
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
import os
import json
import uuid
import logging


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api-service")

redis_client = Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True,
)

TASKS_CREATED = Counter(
    "api_tasks_created_total",
    "Total number of tasks created by the API service",
)

QUEUE_LENGTH = Gauge(
    "api_task_queue_length",
    "Current number of pending tasks in Redis queue",
)

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(
    endpoint="http://jaeger:4317",
    insecure=True,
)

span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

@app.route("/")
def home():
    return jsonify(
        {
            "service": "api-service",
            "message": "Local Microservices Platform API is running",
        }
    )


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/tasks", methods=["POST"])
def create_task():
    with tracer.start_as_current_span("create_task"):
        data = request.get_json() or {}

        task = {
            "id": str(uuid.uuid4()),
            "message": data.get("message", "Default task message"),
            "status": "queued",
        }

        redis_client.lpush("task_queue", json.dumps(task))
        TASKS_CREATED.inc()

        logger.info("Task queued", extra={"task_id": task["id"], "message": task["message"]})

        return jsonify({"message": "Task queued successfully", "task": task}), 201


@app.route("/tasks/queue")
def queue_length():
    length = redis_client.llen("task_queue")
    QUEUE_LENGTH.set(length)

    return jsonify({"queue": "task_queue", "pending_tasks": length})


@app.route("/metrics")
def metrics():
    QUEUE_LENGTH.set(redis_client.llen("task_queue"))
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)