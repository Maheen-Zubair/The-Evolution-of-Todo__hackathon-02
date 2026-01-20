"""
Phase 2 Full-Stack Todo App - FastAPI Dependencies

JWT verification using JWKS from Better Auth.
Supports both Authorization header (Bearer token) and cookies.

Uses PyJWT with PyNaCl for Ed25519 (EdDSA) key support.
"""

import os
from typing import Annotated

import httpx
import jwt
from dotenv import load_dotenv
from fastapi import Cookie, Depends, Header, HTTPException, status
from jwt import PyJWK
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Better Auth JWKS endpoint
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
JWKS_URL = f"{FRONTEND_URL}/api/auth/jwks"

# Cache for JWKS keys
_jwks_cache: dict | None = None
_jwks_cache_time: float = 0
JWKS_CACHE_TTL = 300  # 5 minutes


def fetch_jwks() -> dict:
    """Fetch JWKS from Better Auth endpoint with caching."""
    global _jwks_cache, _jwks_cache_time
    import time

    current_time = time.time()

    # Return cached JWKS if still valid
    if _jwks_cache is not None and (current_time - _jwks_cache_time) < JWKS_CACHE_TTL:
        return _jwks_cache

    try:
        print(f"DEBUG: Fetching JWKS from {JWKS_URL}")
        response = httpx.get(JWKS_URL, timeout=10.0)
        response.raise_for_status()
        _jwks_cache = response.json()
        _jwks_cache_time = current_time
        print(f"DEBUG: JWKS fetched successfully, {len(_jwks_cache.get('keys', []))} keys found")
        return _jwks_cache
    except Exception as e:
        print(f"Error fetching JWKS: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch authentication keys",
        )


def get_signing_key(token: str) -> PyJWK:
    """
    Get the signing key for a token from JWKS.

    Handles cases where JWT doesn't have a 'kid' header by using the first key.
    """
    # Get unverified header to check for kid
    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        print(f"DEBUG: JWT header kid: {kid}")
    except Exception as e:
        print(f"DEBUG: Error getting JWT header: {e}")
        raise

    # Fetch JWKS
    jwks = fetch_jwks()
    keys = jwks.get("keys", [])

    if not keys:
        raise ValueError("No keys found in JWKS")

    # If kid is present, find matching key
    if kid:
        for key_data in keys:
            if key_data.get("kid") == kid:
                return PyJWK.from_dict(key_data)
        # If kid not found, refresh cache and try again
        global _jwks_cache
        _jwks_cache = None
        jwks = fetch_jwks()
        keys = jwks.get("keys", [])
        for key_data in keys:
            if key_data.get("kid") == kid:
                return PyJWK.from_dict(key_data)
        raise ValueError(f"Key with kid '{kid}' not found in JWKS")

    # If no kid in JWT, use the first (and likely only) key
    print(f"DEBUG: No kid in JWT header, using first key from JWKS")
    return PyJWK.from_dict(keys[0])


class TokenData(BaseModel):
    """Extracted data from JWT token."""

    user_id: str
    email: str | None = None


class CurrentUser(BaseModel):
    """Current authenticated user information."""

    id: str
    email: str | None = None


def get_token(
    authorization: Annotated[str | None, Header()] = None,
    better_auth_session_token: Annotated[str | None, Cookie(alias="better-auth.session_token")] = None,
) -> str:
    """
    Extract JWT token from Authorization header or cookie.

    Checks Authorization header first (Bearer token), then falls back to cookie.
    """
    # Try Authorization header first
    if authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            return parts[1]

    # Fall back to cookie
    if better_auth_session_token:
        return better_auth_session_token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


def verify_token(token: str) -> TokenData:
    """
    Verify and decode a Better Auth JWT token using JWKS.

    Uses PyJWT with PyNaCl for Ed25519 (EdDSA) support.

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

    # Debug: Log token prefix to see format
    print(f"DEBUG: Token received (first 50 chars): {token[:50] if len(token) > 50 else token}")
    print(f"DEBUG: Token starts with 'eyJ': {token.startswith('eyJ')}")

    # Check if token looks like a JWT
    if not token.startswith("eyJ"):
        print("DEBUG: Token does not start with 'eyJ', not a valid JWT format")
        raise credentials_exception

    try:
        # Get the signing key from JWKS
        signing_key = get_signing_key(token)
        print(f"DEBUG: Got signing key with algorithm: {signing_key.key_type}")

        # Decode and verify the JWT
        # EdDSA is the algorithm used by Better Auth JWT plugin with Ed25519 keys
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["EdDSA"],
            options={"verify_aud": False},  # Better Auth may not set audience
        )
        print(f"DEBUG: JWT decoded successfully, payload keys: {list(payload.keys())}")

        # Better Auth stores user info in the 'sub' claim
        user_id: str | None = payload.get("sub")
        if user_id is None:
            print("DEBUG: JWT payload missing 'sub' claim")
            raise credentials_exception

        # Email may be in the payload
        email: str | None = payload.get("email")

        print(f"DEBUG: User authenticated: {user_id}")
        return TokenData(user_id=user_id, email=email)

    except InvalidTokenError as e:
        print(f"JWT verification error: {e}")
        raise credentials_exception
    except ValueError as e:
        print(f"Key error: {e}")
        raise credentials_exception
    except Exception as e:
        print(f"Unexpected error during token verification: {e}")
        raise credentials_exception


def get_current_user(
    token: Annotated[str, Depends(get_token)],
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
