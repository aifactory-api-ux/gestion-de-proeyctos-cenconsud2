import os
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from shared.models import (
    Project, Budget, ForecastRequest, ForecastResponse, User, ErrorResponse
)
from api_gateway.service import (
    aggregate_forecast,
    get_project_from_service,
    get_projects_from_service,
    get_budget_from_service,
    get_user_from_service
)

router = APIRouter()
security = HTTPBearer()


async def get_token(authorization: str = Header(None)) -> str:
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if authorization.startswith("Bearer "):
        return authorization[7:]
    return authorization


@router.post(
    "/forecast",
    response_model=ForecastResponse,
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def post_forecast(
    request: ForecastRequest,
    token: str = Depends(get_token)
) -> ForecastResponse:
    return await aggregate_forecast(request, token)


@router.get(
    "/projects/{project_id}",
    response_model=Project,
    responses={404: {"model": ErrorResponse}},
)
async def get_project(project_id: int, token: str = Depends(get_token)) -> Project:
    project = await get_project_from_service(project_id, token)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found"
        )
    return project


@router.get("/projects", response_model=List[Project], responses={500: {"model": ErrorResponse}})
async def get_projects(token: str = Depends(get_token)) -> List[Project]:
    projects = await get_projects_from_service(token)
    return [Project(**p) for p in projects]


@router.get(
    "/budgets/{project_id}",
    response_model=Budget,
    responses={404: {"model": ErrorResponse}},
)
async def get_budget(project_id: int, token: str = Depends(get_token)) -> Budget:
    budget = await get_budget_from_service(project_id, token)
    if budget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Budget for project {project_id} not found"
        )
    return budget


@router.get(
    "/users/me",
    response_model=User,
    responses={401: {"model": ErrorResponse}},
)
async def get_me(token: str = Depends(get_token)) -> User:
    user = await get_user_from_service(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    return user