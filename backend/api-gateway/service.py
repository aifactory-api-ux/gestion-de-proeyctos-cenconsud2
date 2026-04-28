import os
import logging
from datetime import datetime
from typing import Optional

import httpx
from shared.models import ForecastRequest, ForecastResponse, Budget, Project, User
from shared.config import settings

logger = logging.getLogger(__name__)

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
PROJECT_SERVICE_URL = os.getenv("PROJECT_SERVICE_URL", "http://localhost:8002")
BUDGET_SERVICE_URL = os.getenv("BUDGET_SERVICE_URL", "http://localhost:8003")

MOCK_FORECASTS = {
    1: ForecastResponse(
        project_id=1,
        forecasted_cost=98000.0,
        confidence=0.85,
        generated_at=datetime(2024, 3, 15, 12, 0, 0)
    ),
    2: ForecastResponse(
        project_id=2,
        forecasted_cost=73000.0,
        confidence=0.88,
        generated_at=datetime(2024, 3, 15, 12, 0, 0)
    ),
    3: ForecastResponse(
        project_id=3,
        forecasted_cost=190000.0,
        confidence=0.79,
        generated_at=datetime(2024, 3, 15, 12, 0, 0)
    ),
}


async def aggregate_forecast(request: ForecastRequest, token: str) -> ForecastResponse:
    logger.info(f"Aggregating forecast for project {request.project_id}")

    if request.project_id in MOCK_FORECASTS:
        return MOCK_FORECASTS[request.project_id]

    sageMaker_endpoint = settings.SAGEMAKER_ENDPOINT
    logger.info(f"Calling SageMaker endpoint: {sageMaker_endpoint}")

    return ForecastResponse(
        project_id=request.project_id,
        forecasted_cost=75000.0,
        confidence=0.75,
        generated_at=datetime.utcnow()
    )


async def get_project_from_service(project_id: int, token: str) -> Optional[Project]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{PROJECT_SERVICE_URL}/project/projects/{project_id}",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10.0
            )
            if response.status_code == 200:
                data = response.json()
                return Project(**data)
        except Exception as e:
            logger.error(f"Error calling project service: {e}")
    return None


async def get_projects_from_service(token: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{PROJECT_SERVICE_URL}/project/projects",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10.0
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"Error calling project service: {e}")
    return []


async def get_budget_from_service(project_id: int, token: str) -> Optional[Budget]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BUDGET_SERVICE_URL}/budget/budgets/{project_id}",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10.0
            )
            if response.status_code == 200:
                data = response.json()
                return Budget(**data)
        except Exception as e:
            logger.error(f"Error calling budget service: {e}")
    return None


async def get_user_from_service(token: str) -> Optional[User]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/auth/users/me",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10.0
            )
            if response.status_code == 200:
                data = response.json()
                return User(**data)
        except Exception as e:
            logger.error(f"Error calling auth service: {e}")
    return None