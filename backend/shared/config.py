import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "cenconsud2"
    POSTGRES_USER: str = "cenconsud2_user"
    POSTGRES_PASSWORD: str = "supersecret"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    AWS_REGION: str = "us-east-1"
    SAGEMAKER_ENDPOINT: str = "cenconsud2-forecast-prod"
    API_GATEWAY_URL: str = "https://api.cenconsud2.com"

    JWT_SECRET: str = "change-me"
    JWT_EXPIRE_MINUTES: int = 60

    FRONTEND_URL: str = "https://app.cenconsud2.com"
    NODE_ENV: str = "production"
    REACT_APP_API_URL: str = "https://api.cenconsud2.com"

    SQS_QUEUE_URL: str = ""
    SNS_TOPIC_ARN: str = ""

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()