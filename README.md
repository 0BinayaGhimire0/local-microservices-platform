# Local Microservices Platform

A production-style multi-service platform that runs fully locally without using AWS or any cloud provider.

## What This Project Demonstrates

- Multi-service architecture
- API service and background worker service
- Redis-based task queue
- Docker Compose for local orchestration
- Service-to-service communication
- Local development workflow for platform engineering practice

## Tech Stack

- Python
- Flask
- Redis
- Docker
- Docker Compose

## Architecture

```text
Client
  |
  v
API Service
  |
  v
Redis Queue
  |
  v
Worker Service


Kubernetes Local Deployment

This project can also run on a local Kubernetes cluster using Kind.

### Build Images

```bash
docker build -t local-microservices-api:local ./services/api
docker build -t local-microservices-worker:local ./services/worker