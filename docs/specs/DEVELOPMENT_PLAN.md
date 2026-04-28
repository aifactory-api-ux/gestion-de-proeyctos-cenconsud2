# DEVELOPMENT PLAN: gestion de proeyctos Cenconsud2

## 1. ARCHITECTURE OVERVIEW

**System Components:**
- **Backend Microservices (Python 3.11, FastAPI):**
  - **auth-service** (port 8001): User authentication, user info
  - **project-service** (port 8002): Project CRUD, project listing
  - **budget-service** (port 8003): Budget retrieval per project
  - **api-gateway** (port 8004): Aggregates/proxies all endpoints, orchestrates forecasting (calls SageMaker)
- **Frontend (React 18, TypeScript):**
  - Dashboard, project/budget/forecast visualization, user menu
- **Shared Modules:**
  - **backend/shared/**: Pydantic models, DB connection, utilities
  - **frontend/src/types/**: TypeScript interfaces (data contracts)
- **Infrastructure:**
  - PostgreSQL 15 (AWS RDS), Redis 7 (AWS ElastiCache)
  - AWS ECS Fargate, CloudFront, API Gateway, SageMaker, Bedrock, SQS, SNS
  - Docker Compose for local dev, Terraform for IaC, GitHub Actions for CI/CD

**Data Contracts:**  
Defined in `backend/shared/models.py` (Pydantic) and `frontend/src/types/models.ts` (TypeScript).  
**API Endpoints:**  
As specified in SPEC.md §3, strictly enforced.

**Folder Structure:**  
As per SPEC.md §4 and architecture notes, with strict Dockerfile placement and shared code rules.

---

## 2. ACCEPTANCE CRITERIA

1. **End-to-end data flow:** A user can authenticate, view a list of projects, select a project, view its budget and forecast, and see all data visualized in the frontend dashboard, with all data flowing through the API Gateway and backend microservices.
2. **Forecasting integration:** The POST `/forecast` endpoint in the API Gateway triggers a call to SageMaker, returns a valid `ForecastResponse`, and the frontend displays the forecast chart for the selected project.
3. **Infrastructure completeness:** Running `./run.sh` after cloning the repo and setting up `.env` brings up all services (DB, Redis, backend, frontend) with healthchecks, and the web app is accessible at the documented URL, with all endpoints responding as specified.

---

## TEAM SCOPE (MANDATORY — PARSED BY THE PIPELINE)

- **Role:** role-tl (technical_lead)
- **Role:** role-be (backend_developer)
- **Role:** role-fe (frontend_developer)
- **Role:** role-devops (devops_support)

---

## 3. EXECUTABLE ITEMS

---

### ITEM 1: Foundation — shared types, interfaces, DB schemas, config

**Goal:**  
Create all shared code and contracts for backend and frontend, including Pydantic models, TypeScript interfaces, shared DB connection logic, and utility/config files. This includes every model, type, and config that will be imported by any other service or frontend module.

**Files to create:**
- backend/shared/models.py (create) — All Pydantic models: Project, Budget, ForecastRequest, ForecastResponse, User, ErrorResponse (as per SPEC.md §2)
- backend/shared/db.py (create) — Shared PostgreSQL/Redis connection logic (used by all backend services)
- backend/shared/utils.py (create) — Shared utility functions (e.g., date formatting, error handling)
- frontend/src/types/models.ts (create) — TypeScript interfaces for Project, Budget, ForecastRequest, ForecastResponse, User, ErrorResponse (as per SPEC.md §2)
- frontend/src/utils/format.ts (create) — Shared formatting helpers for frontend (dates, currency)
- backend/shared/config.py (create) — Environment variable validation and shared constants for backend (using pydantic-settings)
- frontend/src/config.ts (create) — Frontend config (API URL, env validation)
- backend/shared/requirements.txt (create) — All Python dependencies used by any backend service (fastapi, pydantic, sqlalchemy, psycopg2-binary, redis, python-jose, pydantic-settings, etc.)

**Dependencies:** None

**Validation:**  
- All models/interfaces are importable and match the contracts in SPEC.md.
- Running `python -m backend.shared.models` validates Pydantic models.
- TypeScript interfaces compile with `tsc`.
- Importing config in any backend/FE service validates required env vars.

**Role:** role-tl (technical_lead)

---

### ITEM 2: Auth Service — User authentication and info (GET /users/me)

**Goal:**  
Implement the authentication microservice with FastAPI, providing the `/users/me` endpoint for user info retrieval, JWT validation, and role enforcement. Includes healthcheck, structured logging, and env validation.

**Files to create:**
- backend/auth-service/main.py (create) — FastAPI app entrypoint, includes `/health` and `/users/me`
- backend/auth-service/routes.py (create) — Defines `/users/me` endpoint, JWT dependency
- backend/auth-service/service.py (create) — Business logic for user retrieval and JWT validation
- backend/auth-service/Dockerfile (create) — Multi-stage build, EXPOSE 8001, CMD: uvicorn main:app (context: backend/auth-service)
- backend/auth-service/requirements.txt (create) — Python dependencies (import from shared/requirements.txt if possible)

**Dependencies:** Item 1

**Validation:**  
- `GET /users/me` returns a valid User object when provided a valid JWT.
- `GET /health` returns service status.
- Service starts in Docker and passes healthcheck.

**Role:** role-be (backend_developer)

---

### ITEM 3: Project Service — Project endpoints (GET /projects, GET /projects/{project_id})

**Goal:**  
Implement the project microservice with FastAPI, providing endpoints to list all projects and retrieve a single project by ID. Includes healthcheck, structured logging, and env validation.

**Files to create:**
- backend/project-service/main.py (create) — FastAPI app entrypoint, includes `/health`, `/projects`, `/projects/{project_id}`
- backend/project-service/routes.py (create) — Defines project endpoints
- backend/project-service/service.py (create) — Business logic for project retrieval
- backend/project-service/Dockerfile (create) — Multi-stage build, EXPOSE 8002, CMD: uvicorn main:app (context: backend/project-service)
- backend/project-service/requirements.txt (create) — Python dependencies (import from shared/requirements.txt if possible)

**Dependencies:** Item 1

**Validation:**  
- `GET /projects` returns a list of Project objects.
- `GET /projects/{project_id}` returns a Project or 404.
- `GET /health` returns service status.
- Service starts in Docker and passes healthcheck.

**Role:** role-be (backend_developer)

---

### ITEM 4: Budget Service — Budget endpoint (GET /budgets/{project_id})

**Goal:**  
Implement the budget microservice with FastAPI, providing the endpoint to retrieve budget info for a given project. Includes healthcheck, structured logging, and env validation.

**Files to create:**
- backend/budget-service/main.py (create) — FastAPI app entrypoint, includes `/health`, `/budgets/{project_id}`
- backend/budget-service/routes.py (create) — Defines budget endpoint
- backend/budget-service/service.py (create) — Business logic for budget retrieval
- backend/budget-service/Dockerfile (create) — Multi-stage build, EXPOSE 8003, CMD: uvicorn main:app (context: backend/budget-service)
- backend/budget-service/requirements.txt (create) — Python dependencies (import from shared/requirements.txt if possible)

**Dependencies:** Item 1

**Validation:**  
- `GET /budgets/{project_id}` returns a Budget object or 404.
- `GET /health` returns service status.
- Service starts in Docker and passes healthcheck.

**Role:** role-be (backend_developer)

---

### ITEM 5: API Gateway — Aggregated endpoints (proxy, orchestration, POST /forecast)

**Goal:**  
Implement the API Gateway with FastAPI, exposing all aggregated endpoints as per SPEC.md §3, proxying requests to the appropriate backend services, and orchestrating the `/forecast` endpoint (calls SageMaker). Includes healthcheck, structured logging, and env validation.

**Files to create:**
- backend/api-gateway/main.py (create) — FastAPI app entrypoint, includes `/health` and all aggregated endpoints
- backend/api-gateway/routes.py (create) — Defines all API Gateway endpoints (proxy logic)
- backend/api-gateway/service.py (create) — Orchestration logic, SageMaker integration for `/forecast`
- backend/api-gateway/Dockerfile (create) — Multi-stage build, EXPOSE 8004, CMD: uvicorn main:app (context: backend/api-gateway)
- backend/api-gateway/requirements.txt (create) — Python dependencies (import from shared/requirements.txt if possible)

**Dependencies:** Item 1

**Validation:**  
- All endpoints (`/projects`, `/projects/{project_id}`, `/budgets/{project_id}`, `/users/me`, `/forecast`) proxy correctly and return valid responses.
- `/forecast` triggers SageMaker and returns a valid ForecastResponse.
- `GET /health` returns service status.
- Service starts in Docker and passes healthcheck.

**Role:** role-be (backend_developer)

---

### ITEM 6: Frontend — Dashboard, project/budget/forecast visualization

**Goal:**  
Implement the React frontend, including project list, project details, budget summary, forecast chart, and user menu. Integrate with API Gateway endpoints using Axios client and custom hooks. Includes frontend Dockerfile and startup script.

**Files to create:**
- frontend/public/index.html (create) — HTML entrypoint
- frontend/public/favicon.ico (create) — App icon
- frontend/src/main.tsx (create) — React entrypoint
- frontend/src/App.tsx (create) — Root component, routing/layout
- frontend/src/api/client.ts (create) — Axios API client (uses config)
- frontend/src/api/forecast.ts (create) — Forecast API functions
- frontend/src/hooks/useProjects.ts (create) — Project state hook
- frontend/src/hooks/useBudget.ts (create) — Budget state hook
- frontend/src/hooks/useForecast.ts (create) — Forecast state hook
- frontend/src/components/ProjectList.tsx (create) — Project list UI 
- frontend/src/components/ProjectDetails.tsx (create) — Project details UI
- frontend/src/components/BudgetSummary.tsx (create) — Budget summary UI
- frontend/src/components/ForecastChart.tsx (create) — Forecast visualization
- frontend/src/components/UserMenu.tsx (create) — User info/logout
- frontend/Dockerfile (create) — Multi-stage build, production-ready, exposes frontend
- frontend/package.json (create) — Frontend dependencies and scripts
- frontend/tsconfig.json (create) — TypeScript config
- frontend/start.sh (create) — Frontend startup script

**Dependencies:** Item 1

**Validation:**  
- App builds and runs in Docker.
- User can view project list, select a project, see budget and forecast, and interact with user menu.
- All API calls succeed and data is rendered as per contracts.

**Role:** role-fe (frontend_developer)

---

### ITEM 7: Infrastructure & Deployment

**Goal:**  
Provide complete Docker orchestration and deployment scripts for local development, including all required infra files, healthchecks, and documentation. Ensures zero manual steps: clone → `./run.sh` → working app.

**Files to create:**
- docker-compose.yml (create) — Orchestrates all backend services, frontend, PostgreSQL, Redis, with healthchecks and correct build contexts
- .env.example (create) — Documents all required environment variables with descriptions and example values
- .gitignore (create) — Excludes node_modules, dist, .env, __pycache__, *.pyc, etc.
- .dockerignore (create) — Excludes node_modules, .git, *.log, dist, etc.
- run.sh (create) — Validates Docker, builds, starts, waits for healthy, prints access URL
- README.md (create) — Prerequisites, setup, run instructions, endpoints, troubleshooting
- docs/architecture.md (create) — System diagram and component descriptions

**Dependencies:** All previous items

**Validation:**  
- `./run.sh` completes without errors.
- All services report healthy in Docker Compose.
- Web app accessible at documented URL.
- All API endpoints respond as specified.

**Role:** role-devops (devops_support)

---