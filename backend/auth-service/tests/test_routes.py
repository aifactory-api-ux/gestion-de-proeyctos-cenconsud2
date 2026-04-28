import pytest
import sys
import os
from datetime import datetime
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

sys.modules['shared.db'] = MagicMock()
sys.modules['shared.db'].get_redis_client = MagicMock(return_value=MagicMock())

import main
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    return TestClient(main.app)


class TestAuthServiceHealth:
    def test_health_endpoint(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "auth-service"


class TestAuthServiceRoutes:
    def test_get_me_with_valid_token(self, client):
        response = client.get(
            "/auth/users/me",
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["email"] == "admin@cenconsud2.com"
        assert data["full_name"] == "Admin User"
        assert data["role"] == "admin"

    def test_get_me_with_user_token(self, client):
        response = client.get(
            "/auth/users/me",
            headers={"Authorization": "Bearer user-token"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 2
        assert data["email"] == "user@cenconsud2.com"
        assert data["full_name"] == "Regular User"
        assert data["role"] == "user"

    def test_get_me_without_authorization_header(self, client):
        response = client.get("/auth/users/me")
        assert response.status_code == 403

    def test_get_me_with_invalid_token(self, client):
        response = client.get(
            "/auth/users/me",
            headers={"Authorization": "Bearer invalid-token"}
        )
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
