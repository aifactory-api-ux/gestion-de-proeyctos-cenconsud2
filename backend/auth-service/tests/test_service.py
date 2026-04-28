import pytest
import sys
import os
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

sys.modules['shared.db'] = MagicMock()
sys.modules['shared.db'].get_redis_client = MagicMock(return_value=MagicMock())

import service


class TestCreateAccessToken:
    def test_create_access_token(self):
        token = service.create_access_token({"sub": "1"})
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_with_custom_expiry(self):
        from datetime import timedelta
        token = service.create_access_token({"sub": "1"}, expires_delta=timedelta(minutes=30))
        assert token is not None


class TestDecodeToken:
    def test_decode_valid_token(self):
        token = service.create_access_token({"sub": "1"})
        payload = service.decode_token(token)
        assert payload is not None
        assert payload["sub"] == "1"
        assert "exp" in payload

    def test_decode_invalid_token(self):
        payload = service.decode_token("invalid.token.here")
        assert payload is None


class TestGetUserById:
    def test_get_existing_user(self):
        user = service.get_user_by_id(1)
        assert user is not None
        assert user.id == 1
        assert user.email == "admin@cenconsud2.com"

    def test_get_non_existing_user(self):
        user = service.get_user_by_id(999)
        assert user is None


class TestMockUsers:
    def test_mock_users_defined(self):
        assert "test-token" in service.MOCK_USERS
        assert "user-token" in service.MOCK_USERS

    def test_mock_user_admin(self):
        user = service.MOCK_USERS["test-token"]
        assert user.id == 1
        assert user.role == "admin"

    def test_mock_user_regular(self):
        user = service.MOCK_USERS["user-token"]
        assert user.id == 2
        assert user.role == "user"
