import pytest
import sys
import os
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

sys.modules['shared.db'] = MagicMock()
sys.modules['shared.db'].get_redis_client = MagicMock(return_value=MagicMock())

from shared.config import settings


class TestSettings:
    def test_settings_postgres_defaults(self):
        assert settings.POSTGRES_HOST == "localhost"
        assert settings.POSTGRES_PORT == 5432
        assert settings.POSTGRES_DB == "cenconsud2"
        assert settings.POSTGRES_USER == "cenconsud2_user"

    def test_settings_redis_defaults(self):
        assert settings.REDIS_HOST == "localhost"
        assert settings.REDIS_PORT == 6379

    def test_settings_aws_defaults(self):
        assert settings.AWS_REGION == "us-east-1"
        assert settings.SAGEMAKER_ENDPOINT == "cenconsud2-forecast-prod"

    def test_settings_jwt_defaults(self):
        assert settings.JWT_SECRET == "change-me"
        assert settings.JWT_EXPIRE_MINUTES == 60

    def test_settings_log_level_default(self):
        assert settings.LOG_LEVEL == "INFO"

    def test_settings_environment_defaults(self):
        assert settings.NODE_ENV == "production"
        assert settings.REACT_APP_API_URL == "https://api.cenconsud2.com"
        assert settings.API_GATEWAY_URL == "https://api.cenconsud2.com"
        assert settings.FRONTEND_URL == "https://app.cenconsud2.com"
