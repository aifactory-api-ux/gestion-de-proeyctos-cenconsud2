# Cenconsud2 Project Management

A microservices-based project management system with authentication, project tracking, budget management, and forecasting capabilities.

## Architecture

- **Backend**: Python 3.11, FastAPI microservices
  - auth-service (port 8001): User authentication
  - project-service (port 8002): Project CRUD
  - budget-service (port 8003): Budget retrieval
  - api-gateway (port 8004): API aggregation and orchestration

- **Frontend**: React 18, TypeScript, Vite

- **Infrastructure**: Docker Compose, PostgreSQL 15, Redis 7

## Prerequisites

- Docker 24+
- Docker Compose 1.29+

## Quick Start

1. Clone the repository
2. Copy `.env.example` to `.env` and adjust if needed
3. Run:

```bash
./run.sh
```

4. Access the application at http://localhost:3000

## Services

| Service       | Port | URL                    |
|---------------|------|------------------------|
| Frontend      | 3000 | http://localhost:3000  |
| API Gateway   | 8004 | http://localhost:8004  |
| Auth Service  | 8001 | http://localhost:8001  |
| Project Svc   | 8002 | http://localhost:8002  |
| Budget Svc    | 8003 | http://localhost:8003  |

## API Endpoints

- `POST /forecast` - Get project forecast
- `GET /projects` - List all projects
- `GET /projects/{id}` - Get project details
- `GET /budgets/{project_id}` - Get project budget
- `GET /users/me` - Get current user

## Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild a specific service
docker-compose build <service-name>
```

## Environment Variables

See `.env.example` for all available environment variables.