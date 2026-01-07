"""
Phase 2 Full-Stack Todo App - FastAPI Dependencies

JWT verification and user extraction from Better Auth cookies.
"""

import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Cookie, Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Better Auth configuration
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")

if not BETTER_AUTH_SECRET:
    raise ValueError("BETTER_AUTH_SECRET environment variable is not set")

# Better Auth uses HS256 by default
ALGORITHM = "HS256"


class TokenData(BaseModel):
    """Extracted data from JWT token."""

    user_id: str
    email: str | None = None


class CurrentUser(BaseModel):
    """Current authenticated user information."""

    id: str
    email: str | None = None


def get_token_from_cookie(
    better_auth_session_token: Annotated[str | None, Cookie(alias="better-auth.session_token")] = None,
) -> str:
    """
    Extract the session token from Better Auth cookie.

    Better Auth stores the JWT in a cookie named 'better-auth.session_token'.
    """
    if not better_auth_session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return better_auth_session_token


def verify_token(token: str) -> TokenData:
    """
    Verify and decode a Better Auth JWT token.

    Args:
        token: The JWT token string

    Returns:
        TokenData with user_id and email

    Raises:
        HTTPException: If token is invalid or expired
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])

        # Better Auth stores user info in the 'sub' claim
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        # Email may be in the payload
        email: str | None = payload.get("email")

        return TokenData(user_id=user_id, email=email)

    except JWTError:
        raise credentials_exception


def get_current_user(
    token: Annotated[str, Depends(get_token_from_cookie)],
) -> CurrentUser:
    """
    FastAPI dependency to get the current authenticated user.

    Use with Depends() in route handlers to require authentication:

    Example:
        @app.get("/tasks")
        def list_tasks(current_user: CurrentUser = Depends(get_current_user)):
            # current_user.id is available here
            return {"user_id": current_user.id}
    """
    token_data = verify_token(token)
    return CurrentUser(id=token_data.user_id, email=token_data.email)


# Type alias for cleaner dependency injection
AuthenticatedUser = Annotated[CurrentUser, Depends(get_current_user)]
