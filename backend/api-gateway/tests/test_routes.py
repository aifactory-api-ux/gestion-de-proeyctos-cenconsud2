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


class TestAPIGatewayHealth:
    def test_health_endpoint(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "api-gateway"


class TestAPIGatewayRoutes:
    def test_get_projects_without_token(self, client):
        response = client.get("/projects")
        assert response.status_code == 401

    def test_get_project_without_token(self, client):
        response = client.get("/projects/1")
        assert response.status_code == 401

    def test_get_budget_without_token(self, client):
        response = client.get("/budgets/1")
        assert response.status_code == 401

    def test_post_forecast_without_token(self, client):
        response = client.post("/forecast", json={"project_id": 1})
        assert response.status_code == 401

    def test_get_me_without_token(self, client):
        response = client.get("/users/me")
        assert response.status_code == 401
