"""Authentication Middleware for API."""
from typing import Optional, Callable, Awaitable
import os
from fastapi import Request, Response, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta


class AuthMiddleware:
    """FastAPI middleware for JWT authentication and validation."""

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.security = HTTPBearer(auto_error=False)

    async def __call__(self, request: Request, call_next: Callable):
        """Process incoming requests with authentication."""
        credentials: Optional[HTTPAuthorizationCredentials] = await self.security(request)

        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Missing authorization header"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            payload = jwt.decode(credentials.credentials, self.secret_key, algorithms=[self.algorithm])
            request.state.user_id = payload.get("sub")
            request.state.user_email = payload.get("email")
            request.state.roles = payload.get("roles", [])
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Token has expired"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Invalid token"},
            )

        response = await call_next(request)
        return response


async def verify_token(token: str, secret_key: str) -> dict:
    """Verify JWT token and extract payload."""
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Token has expired"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": str(e)},
        )


async def create_token(user_id: str, email: str, roles: list = None) -> str:
    """Create JWT access token."""
    secret_key = os.getenv("JWT_SECRET_KEY")
    if not secret_key or secret_key == "YOUR_SECRET_KEY":
        raise ValueError(
            "JWT_SECRET_KEY environment variable is required and must be set to a valid secret key"
        )
    payload = {
        "sub": user_id,
        "email": email,
        "roles": roles or [],
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")

