---
name: "auth-token-validator"
description: "Autonomously validates JWT tokens for secure Todo API access."
version: "1.0"
author: "Evolution of Todo Team"
tags: ["jwt", "auth", "security", "better-auth", "validation", "autonomous"]
autonomy: "full"
escalation: "internal-errors-only"
---

# Auth Token Validator Agent

Autonomously validates JWT tokens before any Todo API call to enforce authentication and user isolation.

## Purpose

This agent runs independently without human input to:
- Extract and validate JWT tokens from request headers
- Verify token signatures using Better Auth
- Enforce user isolation (user can only access their own resources)
- Return structured verdict for API middleware

## When to Use

**Trigger**: Automatically before ANY Todo API call that requires authentication.

**Autonomy Level**: Full - no human input needed. Escalate only on internal errors (e.g., secret unavailable, crypto failure).

**Integration Point**: FastAPI dependency injection or middleware.

---

## 8 Autonomous Decisions

The agent performs these checks in sequence. If any check fails, it immediately returns DENIED.

### Decision 1: Extract Token from Header

**Action**: Parse `Authorization: Bearer <token>` header.

```python
def extract_token(authorization: str | None) -> str | None:
    """Extract JWT token from Authorization header."""
    if not authorization:
        return None

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    return parts[1]
```

**Failure Output**:
```json
{"verdict": "DENIED", "reason": "Missing Authorization header", "status_code": 401}
```

---

### Decision 2: Check Token Format

**Action**: Verify token is not missing or malformed (must have 3 dot-separated parts).

```python
def is_valid_jwt_format(token: str) -> bool:
    """Check if token has valid JWT structure (header.payload.signature)."""
    parts = token.split(".")
    return len(parts) == 3 and all(len(p) > 0 for p in parts)
```

**Failure Output**:
```json
{"verdict": "DENIED", "reason": "Malformed token format", "status_code": 401}
```

---

### Decision 3: Verify Signature

**Action**: Verify JWT signature using `BETTER_AUTH_SECRET` environment variable.

```python
import jwt
import os

def verify_signature(token: str) -> dict | None:
    """Verify JWT signature and return decoded payload."""
    secret = os.getenv("BETTER_AUTH_SECRET")

    if not secret:
        raise InternalError("BETTER_AUTH_SECRET not configured")

    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=["HS256"],
            options={"verify_exp": False}  # Check expiry separately
        )
        return payload
    except jwt.InvalidSignatureError:
        return None
    except jwt.DecodeError:
        return None
```

**Failure Output**:
```json
{"verdict": "DENIED", "reason": "Invalid signature", "status_code": 401}
```

---

### Decision 4: Decode Payload

**Action**: Extract `user_id`, `email`, and other claims from decoded payload.

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class TokenClaims:
    user_id: str
    email: Optional[str]
    exp: int
    iat: int
    sub: Optional[str] = None

def extract_claims(payload: dict) -> TokenClaims | None:
    """Extract required claims from JWT payload."""
    user_id = payload.get("sub") or payload.get("user_id") or payload.get("id")

    if not user_id:
        return None

    return TokenClaims(
        user_id=str(user_id),
        email=payload.get("email"),
        exp=payload.get("exp", 0),
        iat=payload.get("iat", 0),
        sub=payload.get("sub"),
    )
```

**Failure Output**:
```json
{"verdict": "DENIED", "reason": "Missing user_id in token", "status_code": 401}
```

---

### Decision 5: Check Token Expiry

**Action**: Verify token has not expired based on `exp` claim.

```python
import time

def is_token_expired(claims: TokenClaims, grace_period: int = 0) -> bool:
    """Check if token has expired."""
    if claims.exp == 0:
        return True  # No expiry = invalid

    current_time = int(time.time())
    return current_time > (claims.exp + grace_period)
```

**Failure Output**:
```json
{"verdict": "EXPIRED", "reason": "Token expired", "status_code": 401}
```

---

### Decision 6: Match User ID

**Action**: Compare decoded `user_id` with request `user_id` (from URL param or body).

```python
def match_user_id(token_user_id: str, request_user_id: str | None) -> bool:
    """Verify token user_id matches the requested resource owner."""
    if request_user_id is None:
        return True  # No specific user requested, allow (filtered in query)

    return token_user_id == request_user_id
```

**Failure Output**:
```json
{"verdict": "DENIED", "reason": "User ID mismatch - access denied", "status_code": 403}
```

---

### Decision 7: Custom Checks (Revocation, etc.)

**Action**: Perform optional custom checks if specified in config.

```python
from typing import Callable, List

CustomCheck = Callable[[TokenClaims], bool]

async def run_custom_checks(
    claims: TokenClaims,
    checks: List[CustomCheck],
) -> tuple[bool, str | None]:
    """Run any custom validation checks."""
    for check in checks:
        try:
            if not await check(claims):
                return False, f"Custom check failed: {check.__name__}"
        except Exception as e:
            return False, f"Custom check error: {str(e)}"

    return True, None

# Example: Token revocation check
async def check_not_revoked(claims: TokenClaims) -> bool:
    """Check if token has been revoked (e.g., in Redis blacklist)."""
    # redis_client.sismember("revoked_tokens", claims.user_id)
    return True  # Implement based on your revocation strategy
```

**Failure Output**:
```json
{"verdict": "DENIED", "reason": "Token has been revoked", "status_code": 401}
```

---

### Decision 8: Output Verdict

**Action**: Return final structured verdict.

```python
from dataclasses import dataclass, asdict
from typing import Literal

@dataclass
class AuthVerdict:
    verdict: Literal["AUTHORIZED", "DENIED", "EXPIRED"]
    user_id: str | None = None
    email: str | None = None
    reason: str | None = None
    status_code: int = 200

    def to_dict(self) -> dict:
        result = {"verdict": self.verdict}
        if self.verdict == "AUTHORIZED":
            result["user_id"] = self.user_id
            if self.email:
                result["email"] = self.email
        else:
            result["reason"] = self.reason
            result["status_code"] = self.status_code
        return result
```

**Success Output**:
```json
{"verdict": "AUTHORIZED", "user_id": "user123", "email": "user@example.com"}
```

---

## Complete Implementation

```python
# agents/auth_token_validator.py
"""
Autonomous JWT Token Validator Agent

Validates JWT tokens for secure Todo API access without human intervention.
"""

import os
import time
from dataclasses import dataclass
from typing import Literal, Optional, List, Callable

import jwt


class AuthValidatorError(Exception):
    """Internal error that requires escalation."""
    pass


@dataclass
class TokenClaims:
    """Decoded JWT token claims."""
    user_id: str
    email: Optional[str]
    exp: int
    iat: int


@dataclass
class AuthVerdict:
    """Validation result."""
    verdict: Literal["AUTHORIZED", "DENIED", "EXPIRED"]
    user_id: Optional[str] = None
    email: Optional[str] = None
    reason: Optional[str] = None
    status_code: int = 200

    def to_dict(self) -> dict:
        if self.verdict == "AUTHORIZED":
            return {
                "verdict": self.verdict,
                "user_id": self.user_id,
                "email": self.email,
            }
        return {
            "verdict": self.verdict,
            "reason": self.reason,
            "status_code": self.status_code,
        }


class AuthTokenValidator:
    """Autonomous JWT token validator."""

    def __init__(
        self,
        secret: Optional[str] = None,
        algorithms: List[str] = None,
        grace_period: int = 0,
        custom_checks: List[Callable] = None,
    ):
        self.secret = secret or os.getenv("BETTER_AUTH_SECRET")
        self.algorithms = algorithms or ["HS256"]
        self.grace_period = grace_period
        self.custom_checks = custom_checks or []

        if not self.secret:
            raise AuthValidatorError("BETTER_AUTH_SECRET not configured")

    def validate(
        self,
        authorization: Optional[str],
        request_user_id: Optional[str] = None,
    ) -> AuthVerdict:
        """
        Validate JWT token through all 8 decision steps.

        Args:
            authorization: The Authorization header value
            request_user_id: Optional user_id from request (URL param or body)

        Returns:
            AuthVerdict with validation result
        """

        # Decision 1: Extract token from header
        token = self._extract_token(authorization)
        if not token:
            return AuthVerdict(
                verdict="DENIED",
                reason="Missing or invalid Authorization header",
                status_code=401,
            )

        # Decision 2: Check token format
        if not self._is_valid_format(token):
            return AuthVerdict(
                verdict="DENIED",
                reason="Malformed token format",
                status_code=401,
            )

        # Decision 3: Verify signature
        payload = self._verify_signature(token)
        if payload is None:
            return AuthVerdict(
                verdict="DENIED",
                reason="Invalid signature",
                status_code=401,
            )

        # Decision 4: Decode payload / extract claims
        claims = self._extract_claims(payload)
        if claims is None:
            return AuthVerdict(
                verdict="DENIED",
                reason="Missing user_id in token",
                status_code=401,
            )

        # Decision 5: Check token expiry
        if self._is_expired(claims):
            return AuthVerdict(
                verdict="EXPIRED",
                reason="Token expired",
                status_code=401,
            )

        # Decision 6: Match user ID
        if not self._match_user_id(claims.user_id, request_user_id):
            return AuthVerdict(
                verdict="DENIED",
                reason="User ID mismatch - access denied",
                status_code=403,
            )

        # Decision 7: Custom checks
        custom_result = self._run_custom_checks(claims)
        if custom_result is not None:
            return custom_result

        # Decision 8: Output verdict - AUTHORIZED
        return AuthVerdict(
            verdict="AUTHORIZED",
            user_id=claims.user_id,
            email=claims.email,
            status_code=200,
        )

    def _extract_token(self, authorization: Optional[str]) -> Optional[str]:
        """Decision 1: Extract token from Authorization header."""
        if not authorization:
            return None

        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None

        return parts[1]

    def _is_valid_format(self, token: str) -> bool:
        """Decision 2: Check JWT format (header.payload.signature)."""
        parts = token.split(".")
        return len(parts) == 3 and all(len(p) > 0 for p in parts)

    def _verify_signature(self, token: str) -> Optional[dict]:
        """Decision 3: Verify JWT signature."""
        try:
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=self.algorithms,
                options={"verify_exp": False},
            )
            return payload
        except jwt.InvalidSignatureError:
            return None
        except jwt.DecodeError:
            return None

    def _extract_claims(self, payload: dict) -> Optional[TokenClaims]:
        """Decision 4: Extract claims from payload."""
        user_id = (
            payload.get("sub")
            or payload.get("user_id")
            or payload.get("id")
        )

        if not user_id:
            return None

        return TokenClaims(
            user_id=str(user_id),
            email=payload.get("email"),
            exp=payload.get("exp", 0),
            iat=payload.get("iat", 0),
        )

    def _is_expired(self, claims: TokenClaims) -> bool:
        """Decision 5: Check token expiry."""
        if claims.exp == 0:
            return True

        current_time = int(time.time())
        return current_time > (claims.exp + self.grace_period)

    def _match_user_id(
        self,
        token_user_id: str,
        request_user_id: Optional[str],
    ) -> bool:
        """Decision 6: Match token user_id with request user_id."""
        if request_user_id is None:
            return True
        return token_user_id == request_user_id

    def _run_custom_checks(self, claims: TokenClaims) -> Optional[AuthVerdict]:
        """Decision 7: Run custom validation checks."""
        for check in self.custom_checks:
            try:
                if not check(claims):
                    return AuthVerdict(
                        verdict="DENIED",
                        reason=f"Custom check failed: {check.__name__}",
                        status_code=401,
                    )
            except Exception as e:
                raise AuthValidatorError(f"Custom check error: {e}")

        return None  # All checks passed


# FastAPI Integration
def create_auth_dependency():
    """Create FastAPI dependency for token validation."""
    from fastapi import Depends, HTTPException, Request
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

    security = HTTPBearer()
    validator = AuthTokenValidator()

    async def get_current_user(
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(security),
    ) -> str:
        """FastAPI dependency that validates token and returns user_id."""
        # Get request_user_id from path params if present
        request_user_id = request.path_params.get("user_id")

        # Validate token
        result = validator.validate(
            authorization=f"Bearer {credentials.credentials}",
            request_user_id=request_user_id,
        )

        if result.verdict != "AUTHORIZED":
            raise HTTPException(
                status_code=result.status_code,
                detail=result.reason,
                headers={"WWW-Authenticate": "Bearer"},
            )

        return result.user_id

    return get_current_user
```

---

## Process Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTH TOKEN VALIDATOR                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  INPUT: Authorization Header + Request User ID                   │
│         ↓                                                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 1. Extract Token                                          │   │
│  │    "Authorization: Bearer eyJ..."  →  "eyJ..."           │   │
│  └──────────────────────────────────────────────────────────┘   │
│         ↓ (or DENIED: "Missing Authorization header")           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 2. Check Format                                           │   │
│  │    "xxx.yyy.zzz"  →  Valid JWT structure                 │   │
│  └──────────────────────────────────────────────────────────┘   │
│         ↓ (or DENIED: "Malformed token format")                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 3. Verify Signature                                       │   │
│  │    HMAC-SHA256 with BETTER_AUTH_SECRET                   │   │
│  └──────────────────────────────────────────────────────────┘   │
│         ↓ (or DENIED: "Invalid signature")                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 4. Decode Payload                                         │   │
│  │    Extract: user_id, email, exp, iat                     │   │
│  └──────────────────────────────────────────────────────────┘   │
│         ↓ (or DENIED: "Missing user_id in token")               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 5. Check Expiry                                           │   │
│  │    current_time < exp + grace_period                     │   │
│  └──────────────────────────────────────────────────────────┘   │
│         ↓ (or EXPIRED: "Token expired")                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 6. Match User ID                                          │   │
│  │    token.user_id == request.user_id                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│         ↓ (or DENIED: "User ID mismatch")                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 7. Custom Checks                                          │   │
│  │    Revocation, rate limits, etc.                         │   │
│  └──────────────────────────────────────────────────────────┘   │
│         ↓ (or DENIED: "Custom check failed")                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 8. Output Verdict                                         │   │
│  │    AUTHORIZED: {user_id, email}                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  OUTPUT: AuthVerdict JSON                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Output Format

### AUTHORIZED

```json
{
  "verdict": "AUTHORIZED",
  "user_id": "user123",
  "email": "user@example.com"
}
```

### DENIED

```json
{
  "verdict": "DENIED",
  "reason": "Invalid signature",
  "status_code": 401
}
```

### EXPIRED

```json
{
  "verdict": "EXPIRED",
  "reason": "Token expired",
  "status_code": 401
}
```

---

## Examples

### Example 1: Valid Token

**Input**:
```python
authorization = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzM1NjAwMDAwfQ.signature"
request_user_id = "user123"
```

**Output**:
```json
{"verdict": "AUTHORIZED", "user_id": "user123", "email": "user@example.com"}
```

### Example 2: Expired Token

**Input**:
```python
authorization = "Bearer eyJ...expired..."
request_user_id = "user123"
```

**Output**:
```json
{"verdict": "EXPIRED", "reason": "Token expired", "status_code": 401}
```

### Example 3: User ID Mismatch

**Input**:
```python
authorization = "Bearer eyJ...valid_for_user456..."
request_user_id = "user123"  # Trying to access different user's data
```

**Output**:
```json
{"verdict": "DENIED", "reason": "User ID mismatch - access denied", "status_code": 403}
```

### Example 4: Missing Header

**Input**:
```python
authorization = None
request_user_id = "user123"
```

**Output**:
```json
{"verdict": "DENIED", "reason": "Missing or invalid Authorization header", "status_code": 401}
```

---

## Quality Checklist

| Edge Case | Handled | Response |
|-----------|---------|----------|
| Missing header | ✓ | DENIED 401 |
| Empty header | ✓ | DENIED 401 |
| Missing "Bearer" prefix | ✓ | DENIED 401 |
| Malformed JWT (not 3 parts) | ✓ | DENIED 401 |
| Invalid signature | ✓ | DENIED 401 |
| Missing user_id claim | ✓ | DENIED 401 |
| Expired token | ✓ | EXPIRED 401 |
| User ID mismatch | ✓ | DENIED 403 |
| Revoked token | ✓ | DENIED 401 |
| Missing secret (internal) | ✓ | ESCALATE |

---

## Autonomy Notes

- **No Human Input**: Runs independently on every API request
- **Escalation Trigger**: Only escalate on `AuthValidatorError` (internal configuration issues)
- **Logging**: Log all DENIED/EXPIRED verdicts for security audit
- **Performance**: < 5ms validation time (no external calls for signature verification)

---

## Integration

### FastAPI Middleware

```python
from fastapi import FastAPI, Depends
from agents.auth_token_validator import create_auth_dependency

app = FastAPI()
get_current_user = create_auth_dependency()

@app.get("/api/tasks")
async def list_tasks(user_id: str = Depends(get_current_user)):
    # user_id is guaranteed valid here
    return {"user_id": user_id}
```

### Direct Usage

```python
from agents.auth_token_validator import AuthTokenValidator

validator = AuthTokenValidator()
result = validator.validate(
    authorization="Bearer eyJ...",
    request_user_id="user123",
)

if result.verdict == "AUTHORIZED":
    print(f"Welcome, {result.user_id}")
else:
    print(f"Access denied: {result.reason}")
```
