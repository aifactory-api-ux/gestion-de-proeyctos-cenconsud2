from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from shared.models import User

security = HTTPBearer()

JWT_SECRET = "change-me"
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60

MOCK_USERS = {
    "test-token": User(
        id=1,
        email="admin@cenconsud2.com",
        full_name="Admin User",
        role="admin"
    ),
    "user-token": User(
        id=2,
        email="user@cenconsud2.com",
        full_name="Regular User",
        role="user"
    ),
}


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=JWT_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    token = credentials.credentials

    if token in MOCK_USERS:
        return MOCK_USERS[token]

    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    mock_users = {
        1: User(id=1, email="admin@cenconsud2.com", full_name="Admin User", role="admin"),
        2: User(id=2, email="user@cenconsud2.com", full_name="Regular User", role="user"),
    }
    user = mock_users.get(int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_user_by_id(user_id: int) -> Optional[User]:
    mock_users = {
        1: User(id=1, email="admin@cenconsud2.com", full_name="Admin User", role="admin"),
        2: User(id=2, email="user@cenconsud2.com", full_name="Regular User", role="user"),
    }
    return mock_users.get(user_id)