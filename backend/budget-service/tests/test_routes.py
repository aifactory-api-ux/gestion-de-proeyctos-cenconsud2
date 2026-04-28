import pytest
import sys
import os
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

sys.modules['shared.db'] = MagicMock()
sys.modules['shared.db'].get_redis_client = MagicMock(return_value=MagicMock())

import main
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    return TestClient(main.app)


class TestBudgetServiceHealth:
    def test_health_endpoint(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "budget-service"


class TestBudgetServiceRoutes:
    def test_get_existing_budget(self, client):
        response = client.get("/budget/budgets/1")
        assert response.status_code == 200
        data = response.json()
        assert data["project_id"] == 1
        assert data["allocated_amount"] == 100000.0
        assert data["spent_amount"] == 45000.0
        assert data["forecasted_amount"] == 95000.0

    def test_get_existing_budget_project_2(self, client):
        response = client.get("/budget/budgets/2")
        assert response.status_code == 200
        data = response.json()
        assert data["project_id"] == 2
        assert data["allocated_amount"] == 75000.0

    def test_get_existing_budget_project_3(self, client):
        response = client.get("/budget/budgets/3")
        assert response.status_code == 200
        data = response.json()
        assert data["project_id"] == 3
        assert data["allocated_amount"] == 200000.0

    def test_get_non_existing_budget(self, client):
        response = client.get("/budget/budgets/999")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
