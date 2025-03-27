# ADR 001: Microservices Architecture

## Status
Accepted

## Context
Need to independently scale:
- Image processing
- ML model serving
- LLM integration

## Decision
Use Spring Boot microservices with:
- API Gateway routing
- Pub/Sub for async communication
- Kubernetes orchestration

## Consequences
- ✅ Better scalability
- ✅ Independent deployment
- ❄️ Increased operational complexity