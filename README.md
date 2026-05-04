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

CI Pipeline

This project includes a GitHub Actions CI pipeline that validates the platform on every push and pull request.

The pipeline checks:

- API service Python syntax
- Worker service Python syntax
- API Docker image build
- Worker Docker image build
- Kubernetes manifest validation using kubectl dry-run

This demonstrates a CI workflow for a local multi-service platform without using any cloud provider.