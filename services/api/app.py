from flask import Flask, jsonify, request
from redis import Redis
import os
import json
import uuid


app = Flask(__name__)

redis_client = Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True,
)


@app.route("/")
def home():
    return jsonify({
        "service": "api-service",
        "message": "Local Microservices Platform API is running"
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json() or {}

    task = {
        "id": str(uuid.uuid4()),
        "message": data.get("message", "Default task message"),
        "status": "queued"
    }

    redis_client.lpush("task_queue", json.dumps(task))

    return jsonify({
        "message": "Task queued successfully",
        "task": task
    }), 201


@app.route("/tasks/queue")
def queue_length():
    length = redis_client.llen("task_queue")

    return jsonify({
        "queue": "task_queue",
        "pending_tasks": length
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)