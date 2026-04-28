from fastapi import APIRouter, HTTPException, status

from shared.models import Budget, ErrorResponse
from service import get_budget_by_project_id

router = APIRouter()


@router.get("/budgets/{project_id}", response_model=Budget, responses={404: {"model": ErrorResponse}})
async def get_budget(project_id: int) -> Budget:
    budget = get_budget_by_project_id(project_id)
    if budget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Budget for project {project_id} not found"
        )
    return budget