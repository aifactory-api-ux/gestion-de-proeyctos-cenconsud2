#!/bin/bash
set -e

echo "=== Cenconsud2 Project Management - Startup Script ==="

command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed. Aborting." >&2; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "Docker Compose is required but not installed. Aborting." >&2; exit 1; }

echo "Building and starting all services..."

docker-compose build --parallel
docker-compose up -d

echo ""
echo "Waiting for services to become healthy..."

sleep 10

check_service() {
    local port=$1
    local name=$2
    for i in {1..30}; do
        if curl -sf "http://localhost:$port/health" > /dev/null 2>&1; then
            echo "✓ $name is healthy"
            return 0
        fi
        sleep 2
    done
    echo "✗ $name failed to become healthy"
    return 1
}

check_service 8001 "auth-service" &
check_service 8002 "project-service" &
check_service 8003 "budget-service" &
check_service 8004 "api-gateway" &
check_service 3000 "frontend" &
wait

echo ""
echo "=== All services started successfully ==="
echo "Frontend: http://localhost:3000"
echo "API Gateway: http://localhost:8004"
echo "Auth Service: http://localhost:8001"
echo "Project Service: http://localhost:8002"
echo "Budget Service: http://localhost:8003"
echo ""
echo "Run 'docker-compose logs -f' to view logs"
echo "Run 'docker-compose down' to stop all services"