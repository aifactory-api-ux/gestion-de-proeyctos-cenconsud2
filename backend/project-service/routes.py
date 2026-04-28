from fastapi import APIRouter, HTTPException, status
from typing import List

from shared.models import Project, ErrorResponse
from project_service.service import list_projects, get_project_by_id

router = APIRouter()


@router.get("/projects", response_model=List[Project], responses={500: {"model": ErrorResponse}})
async def get_projects() -> List[Project]:
    return list_projects()


@router.get("/projects/{project_id}", response_model=Project, responses={404: {"model": ErrorResponse}})
async def get_project(project_id: int) -> Project:
    project = get_project_by_id(project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found"
        )
    return project