import pytest
import sys
import os
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

sys.modules['shared.db'] = MagicMock()
sys.modules['shared.db'].get_redis_client = MagicMock(return_value=MagicMock())

from shared.models import Project, Budget, ForecastRequest, ForecastResponse, User, ErrorResponse
from datetime import date, datetime


class TestProjectModel:
    def test_project_creation(self):
        project = Project(
            id=1,
            name="Test Project",
            description="A test project",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            manager_id=1,
            status="active"
        )
        assert project.id == 1
        assert project.name == "Test Project"
        assert project.description == "A test project"
        assert project.start_date == date(2024, 1, 1)
        assert project.end_date == date(2024, 12, 31)
        assert project.manager_id == 1
        assert project.status == "active"

    def test_project_optional_description(self):
        project = Project(
            id=2,
            name="No Description",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            manager_id=1,
            status="planning"
        )
        assert project.description is None


class TestBudgetModel:
    def test_budget_creation(self):
        budget = Budget(
            id=1,
            project_id=1,
            allocated_amount=100000.0,
            spent_amount=45000.0,
            forecasted_amount=95000.0,
            last_updated=datetime(2024, 3, 15, 10, 30, 0)
        )
        assert budget.id == 1
        assert budget.project_id == 1
        assert budget.allocated_amount == 100000.0
        assert budget.spent_amount == 45000.0
        assert budget.forecasted_amount == 95000.0
        assert budget.last_updated == datetime(2024, 3, 15, 10, 30, 0)


class TestForecastRequest:
    def test_forecast_request_creation(self):
        request = ForecastRequest(project_id=1)
        assert request.project_id == 1


class TestForecastResponse:
    def test_forecast_response_creation(self):
        response = ForecastResponse(
            project_id=1,
            forecasted_cost=98000.0,
            confidence=0.85,
            generated_at=datetime(2024, 3, 15, 12, 0, 0)
        )
        assert response.project_id == 1
        assert response.forecasted_cost == 98000.0
        assert response.confidence == 0.85
        assert response.generated_at == datetime(2024, 3, 15, 12, 0, 0)


class TestUserModel:
    def test_user_creation(self):
        user = User(
            id=1,
            email="test@example.com",
            full_name="Test User",
            role="admin"
        )
        assert user.id == 1
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.role == "admin"


class TestErrorResponse:
    def test_error_response_creation(self):
        error = ErrorResponse(detail="Not found")
        assert error.detail == "Not found"
