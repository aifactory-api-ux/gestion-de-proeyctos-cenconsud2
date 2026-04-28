from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from shared.models import User, ErrorResponse
from service import get_current_user

router = APIRouter()
security = HTTPBearer()


@router.get(
    "/users/me",
    response_model=User,
    responses={401: {"model": ErrorResponse}},
)
async def get_me(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    token = credentials.credentials

    mock_users = {
        "test-token": User(id=1, email="admin@cenconsud2.com", full_name="Admin User", role="admin"),
        "user-token": User(id=2, email="user@cenconsud2.com", full_name="Regular User", role="user"),
    }

    if token in mock_users:
        return mock_users[token]

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )