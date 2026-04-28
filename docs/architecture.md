# Cenconsud2 Architecture

## System Overview

Cenconsud2 is a microservices-based project management platform built with Python (FastAPI) backend and React frontend.

## Component Diagram

```
                    ┌─────────────┐
                    │   Client    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Frontend   │  (React, Port 3000)
                    │   (Vite)    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ API Gateway │  (FastAPI, Port 8004)
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    ┌───────────┐   ┌───────────┐   ┌───────────┐
    │    Auth   │   │  Project │   │  Budget   │
    │  Service  │   │  Service  │   │  Service  │
    │  (8001)   │   │  (8002)   │   │  (8003)   │
    └───────────┘   └───────────┘   └───────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  SageMaker  │
                    │  (Forecast) │
                    └─────────────┘
```

## Services

### API Gateway (Port 8004)
- Entry point for all frontend requests
- Aggregates data from backend services
- Orchestrates forecast calls to AWS SageMaker
- Handles authentication token validation

### Auth Service (Port 8001)
- User authentication
- JWT token generation and validation
- User info retrieval (`/users/me`)

### Project Service (Port 8002)
- Project CRUD operations
- Project listing (`GET /projects`)
- Project details (`GET /projects/{id}`)

### Budget Service (Port 8003)
- Budget retrieval per project (`GET /budgets/{project_id}`)
- Budget data aggregation

### Frontend (Port 3000)
- React 18 with TypeScript
- Vite for bundling
- Components for project list, details, budget, forecast

## Data Flow

1. User authenticates via `/users/me` through API Gateway
2. API Gateway proxies to Auth Service
3. User views project list via `/projects`
4. API Gateway proxies to Project Service
5. User selects project and views budget via `/budgets/{id}`
6. User requests forecast via `/forecast`
7. API Gateway orchestrates call to SageMaker
8. Forecast data returned and displayed in frontend

## Infrastructure

- **Database**: PostgreSQL 15 (AWS RDS)
- **Cache**: Redis 7 (AWS ElastiCache)
- **Containers**: Docker with Docker Compose
- **Cloud**: AWS ECS Fargate, API Gateway, SageMaker, SQS, SNS

## Security

- JWT-based authentication
- Bearer token in Authorization header
- Service-to-service communication via internal URLs
- Environment variables for sensitive config

## Deployment

Local development uses Docker Compose with healthchecks. Production deployment uses AWS ECS Fargate with Terraform for infrastructure as code.