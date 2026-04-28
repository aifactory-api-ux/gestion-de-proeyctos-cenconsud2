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


class TestProjectServiceHealth:
    def test_health_endpoint(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "project-service"


class TestProjectServiceRoutes:
    def test_get_all_projects(self, client):
        response = client.get("/project/projects")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3

    def test_get_existing_project(self, client):
        response = client.get("/project/projects/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Project Alpha"
        assert data["status"] == "active"

    def test_get_project_2(self, client):
        response = client.get("/project/projects/2")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 2
        assert data["name"] == "Project Beta"
        assert data["status"] == "active"

    def test_get_project_3(self, client):
        response = client.get("/project/projects/3")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 3
        assert data["name"] == "Project Gamma"
        assert data["status"] == "planning"

    def test_get_non_existing_project(self, client):
        response = client.get("/project/projects/999")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
