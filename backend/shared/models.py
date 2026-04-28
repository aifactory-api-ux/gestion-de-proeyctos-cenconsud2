from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime


class Project(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
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