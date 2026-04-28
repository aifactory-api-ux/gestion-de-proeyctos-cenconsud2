# SPEC.md

## 1. TECHNOLOGY STACK

- **Backend**
  - Python 3.11
  - FastAPI 0.110
  - Node.js 20
  - NestJS 10
  - PostgreSQL 15 (AWS RDS)
  - Redis 7 (AWS ElastiCache)
  - AWS SageMaker (ML inference)
  - AWS Bedrock (future LLM integration)
  - AWS SQS (event queue)
  - AWS SNS (notifications)
  - AWS API Gateway (REST endpoint aggregation)
  - Docker 24
  - Terraform 1.6 (infra as code)
- **Frontend**
  - React 18.2
  - TypeScript 5.3
  - Node.js 20
- **Deployment/Infra**
  - AWS ECS Fargate (container orchestration)
  - AWS CloudFront (CDN)
  - Docker Compose (local dev)
  - GitHub Actions (CI/CD)

---

## 2. DATA CONTRACTS

### Python (Pydantic Models)

```python
# backend/shared/models.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime

class Project(BaseModel):
    id: int
    name: str
    description: Optional[str]
    start_date: date
    end_date: date
    manager_id: int
    status: str

class Budget(BaseModel):
    id: int
    project_id: int
    allocated_amount: float
    spent_amount: float
    forecasted_amount: float
    last_updated: datetime

class ForecastRequest(BaseModel):
    project_id: int

class ForecastResponse(BaseModel):
    project_id: int
    forecasted_cost: float
    confidence: float
    generated_at: datetime

class User(BaseModel):
    id: int
    email: str
    full_name: str
    role: str

class ErrorResponse(BaseModel):
    detail: str
```

### TypeScript (Frontend Interfaces)

```typescript
// src/types/models.ts

export interface Project {
  id: number;
  name: string;
  description?: string;
  start_date: string; // ISO date
  end_date: string;   // ISO date
  manager_id: number;
  status: string;
}

export interface Budget {
  id: number;
  project_id: number;
  allocated_amount: number;
  spent_amount: number;
  forecasted_amount: number;
  last_updated: string; // ISO datetime
}

export interface ForecastRequest {
  project_id: number;
}

export interface ForecastResponse {
  project_id: number;
  forecasted_cost: number;
  confidence: number;
  generated_at: string; // ISO datetime
}

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: string;
}

export interface ErrorResponse {
  detail: string;
}
```

---

## 3. API ENDPOINTS

### API Gateway (Aggregated Endpoints)

#### POST `/forecast`
- **Request Body:** `ForecastRequest`
- **Response:** `ForecastResponse`
- **Errors:** `ErrorResponse` (400, 404, 500)

#### GET `/projects/{project_id}`
- **Response:** `Project`
- **Errors:** `ErrorResponse` (404)

#### GET `/projects`
- **Response:** `List[Project]`
- **Errors:** `ErrorResponse` (500)

#### GET `/budgets/{project_id}`
- **Response:** `Budget`
- **Errors:** `ErrorResponse` (404)

#### GET `/users/me`
- **Response:** `User`
- **Errors:** `ErrorResponse` (401)

---

### Backend Service Endpoints

#### Project Service (`backend/project-service/`)
- `GET /projects/{project_id}` → `Project`
- `GET /projects` → `List[Project]`

#### Budget Service (`backend/budget-service/`)
- `GET /budgets/{project_id}` → `Budget`

#### Forecast Service (API Gateway → SageMaker)
- `POST /forecast` → `ForecastResponse`

#### Auth Service (`backend/auth-service/`)
- `GET /users/me` → `User`

---

## 4. FILE STRUCTURE

### PORT TABLE

| Service              | Listening Port | Path                        |
|----------------------|---------------|-----------------------------|
| auth-service         | 8001          | backend/auth-service/       |
| project-service      | 8002          | backend/project-service/    |
| budget-service       | 8003          | backend/budget-service/     |
| api-gateway          | 8004          | backend/api-gateway/        |

### SHARED MODULES

| Shared path          | Imported by services                                 |
|----------------------|-----------------------------------------------------|
| backend/shared/      | auth-service, project-service, budget-service, api-gateway |

---

### FILE TREE

```
.
├── docker-compose.yml                # Local dev orchestration for all services
├── .env.example                     # Template for all required environment variables
├── .gitignore                       # Git ignore rules
├── README.md                        # Project documentation
├── run.sh                           # Root startup script for local dev
├── terraform/
│   ├── main.tf                      # Terraform root config
│   ├── variables.tf                 # Terraform variables
│   ├── outputs.tf                   # Terraform outputs
│   └── provider.tf                  # AWS provider config
├── backend/
│   ├── shared/
│   │   ├── models.py                # Pydantic models (shared contracts)
│   │   ├── db.py                    # Shared DB connection logic
│   │   └── utils.py                 # Shared utility functions
│   ├── auth-service/
│   │   ├── main.py                  # FastAPI app entrypoint
│   │   ├── routes.py                # Auth endpoints
│   │   ├── service.py               # Auth business logic
│   │   ├── Dockerfile               # Auth service Dockerfile (EXPOSE 8001)
│   │   └── requirements.txt         # Python dependencies
│   ├── project-service/
│   │   ├── main.py                  # FastAPI app entrypoint
│   │   ├── routes.py                # Project endpoints
│   │   ├── service.py               # Project business logic
│   │   ├── Dockerfile               # Project service Dockerfile (EXPOSE 8002)
│   │   └── requirements.txt         # Python dependencies
│   ├── budget-service/
│   │   ├── main.py                  # FastAPI app entrypoint
│   │   ├── routes.py                # Budget endpoints
│   │   ├── service.py               # Budget business logic
│   │   ├── Dockerfile               # Budget service Dockerfile (EXPOSE 8003)
│   │   └── requirements.txt         # Python dependencies
│   ├── api-gateway/
│   │   ├── main.py                  # FastAPI app entrypoint
│   │   ├── routes.py                # Aggregated endpoints (proxy to services)
│   │   ├── service.py               # Gateway orchestration logic
│   │   ├── Dockerfile               # API Gateway Dockerfile (EXPOSE 8004)
│   │   └── requirements.txt         # Python dependencies
│   └── start.sh                     # Backend startup script
├── frontend/
│   ├── public/
│   │   ├── index.html               # HTML entrypoint
│   │   └── favicon.ico              # App icon
│   ├── src/
│   │   ├── main.tsx                 # React entrypoint
│   │   ├── App.tsx                  # Root component
│   │   ├── api/
│   │   │   ├── client.ts            # Axios API client
│   │   │   └── forecast.ts          # Forecast API functions
│   │   ├── hooks/
│   │   │   ├── useProjects.ts       # Project state hook
│   │   │   ├── useBudget.ts         # Budget state hook
│   │   │   └── useForecast.ts       # Forecast state hook
│   │   ├── components/
│   │   │   ├── ProjectList.tsx      # Project list UI
│   │   │   ├── ProjectDetails.tsx   # Project details UI
│   │   │   ├── BudgetSummary.tsx    # Budget summary UI
│   │   │   ├── ForecastChart.tsx    # Forecast visualization
│   │   │   └── UserMenu.tsx         # User info/logout
│   │   ├── types/
│   │   │   └── models.ts            # TypeScript interfaces (data contracts)
│   │   └── utils/
│   │       └── format.ts            # Formatting helpers
│   ├── Dockerfile                   # Frontend Dockerfile
│   ├── package.json                 # Frontend dependencies
│   ├── tsconfig.json                # TypeScript config
│   └── start.sh                     # Frontend startup script
├── .github/
│   └── workflows/
│       └── ci.yml                   # GitHub Actions CI/CD pipeline
```

---

## 5. ENVIRONMENT VARIABLES

| Name                        | Type    | Description                                         | Example Value                |
|-----------------------------|---------|-----------------------------------------------------|-----------------------------|
| POSTGRES_HOST               | string  | PostgreSQL hostname                                 | cenconsud2-db.xxxx.rds.amazonaws.com |
| POSTGRES_PORT               | int     | PostgreSQL port                                     | 5432                        |
| POSTGRES_DB                 | string  | PostgreSQL database name                            | cenconsud2                  |
| POSTGRES_USER               | string  | PostgreSQL username                                 | cenconsud2_user             |
| POSTGRES_PASSWORD           | string  | PostgreSQL password                                 | supersecret                 |
| REDIS_HOST                  | string  | Redis hostname                                      | cenconsud2-redis.xxxx.cache.amazonaws.com |
| REDIS_PORT                  | int     | Redis port                                          | 6379                        |
| AWS_REGION                  | string  | AWS region for all services                         | us-east-1                   |
| SAGEMAKER_ENDPOINT          | string  | SageMaker endpoint name                             | cenconsud2-forecast-prod    |
| API_GATEWAY_URL             | string  | API Gateway base URL                                | https://api.cenconsud2.com  |
| JWT_SECRET                  | string  | JWT signing secret for auth-service                 | change-me                   |
| JWT_EXPIRE_MINUTES          | int     | JWT expiration in minutes                           | 60                          |
| FRONTEND_URL                | string  | Public frontend URL                                 | https://app.cenconsud2.com  |
| NODE_ENV                    | string  | Node environment (frontend)                         | production                  |
| REACT_APP_API_URL           | string  | API base URL for frontend                           | https://api.cenconsud2.com  |
| SQS_QUEUE_URL               | string  | AWS SQS queue URL                                   | https://sqs.us-east-1.amazonaws.com/xxx/queue |
| SNS_TOPIC_ARN               | string  | AWS SNS topic ARN                                   | arn:aws:sns:us-east-1:xxx:topic |
| LOG_LEVEL                   | string  | Logging level                                       | INFO                        |

---

## 6. IMPORT CONTRACTS

### Backend (Python)

- `from shared.models import Project, Budget, ForecastRequest, ForecastResponse, User, ErrorResponse`
- `from shared.db import get_db_session`
- `from shared.utils import cache_result, format_currency`

#### Service-specific
- `from service import get_current_user` (auth-service)
- `from service import get_project_by_id, list_projects` (project-service)
- `from service import get_budget_by_project_id` (budget-service)
- `from service import aggregate_forecast` (api-gateway)

### Frontend (TypeScript)

- `import { Project, Budget, ForecastRequest, ForecastResponse, User, ErrorResponse } from '../types/models'`
- `import { useProjects } from '../hooks/useProjects'`
- `import { useBudget } from '../hooks/useBudget'`
- `import { useForecast } from '../hooks/useForecast'`
- `import { getForecast } from '../api/forecast'`
- `import { formatCurrency } from '../utils/format'`

---

## 7. FRONTEND STATE & COMPONENT CONTRACTS

### React Hooks

- `useProjects() → { projects: Project[], loading: boolean, error: string | null, fetchProjects: () => void, getProject: (id: number) => Project | undefined }`
- `useBudget(projectId: number) → { budget: Budget | null, loading: boolean, error: string | null, fetchBudget: () => void }`
- `useForecast(projectId: number) → { forecast: ForecastResponse | null, loading: boolean, error: string | null, fetchForecast: () => void }`

### Reusable Components

- `ProjectList` props: `{ projects: Project[], onSelect: (id: number) => void, selectedId: number | null }`
- `ProjectDetails` props: `{ project: Project, onRequestForecast: (projectId: number) => void }`
- `BudgetSummary` props: `{ budget: Budget | null }`
- `ForecastChart` props: `{ forecast: ForecastResponse | null }`
- `UserMenu` props: `{ user: User, onLogout: () => void }`

---

## 8. FILE EXTENSION CONVENTION

- **Frontend files:** `.tsx` (TypeScript React)
- **Project language:** TypeScript (frontend), Python (backend)
- **Entry point:** `/src/main.tsx` (as referenced in `public/index.html`)

---

**All field names, types, and exported property names must match exactly as specified above. All Dockerfiles for backend services must EXPOSE and CMD on the port assigned in the PORT TABLE. All shared modules under `backend/shared/` must be copied into every backend service image. All environment variables must be present in `.env.example` and referenced verbatim in code.**