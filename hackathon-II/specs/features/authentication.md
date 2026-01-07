---
title: User Authentication with JWT for Multi-User Todo App
description: Secure user signup, signin, and protected access using Better Auth and stateless JWT tokens.
version: "1.0"
status: draft
phase: 2
feature: authentication
created: 2025-12-29
updated: 2025-12-29
authors:
  - Evolution of Todo Team
tags:
  - authentication
  - jwt
  - better-auth
  - security
  - multi-user
dependencies:
  - better-auth
  - next.js
  - fastapi
related:
  - specs/api/rest-endpoints.md
  - specs/database/schema.md
---

# User Authentication with JWT for Multi-User Todo App

## Overview

Secure user signup, signin, and protected access using Better Auth and stateless JWT tokens.

**Target Audience**: Backend and frontend developers implementing secure multi-user access

**Focus**: Stateless authentication, user isolation, token issuance and verification

## Success Criteria

| ID | Criterion | Measurable Outcome |
|----|-----------|-------------------|
| SC-001 | Users can successfully signup | New user record created, JWT returned |
| SC-002 | Users can successfully signin | Valid credentials return JWT token |
| SC-003 | Valid JWT grants access | Protected routes return 200 with data |
| SC-004 | Invalid tokens rejected | Returns 401 Unauthorized |
| SC-005 | Expired tokens rejected | Returns 401 with "Token expired" message |
| SC-006 | User isolation enforced | Tasks filtered by authenticated user_id |
| SC-007 | Stateless backend | No session storage on server |

## Constraints

| Constraint | Requirement |
|------------|-------------|
| Auth Library | Better Auth with JWT plugin in Next.js |
| Token Signing | Shared `BETTER_AUTH_SECRET` environment variable |
| Token Expiry | 7 days default lifetime |
| Token Storage | httpOnly cookie (set by Better Auth, automatic on requests) |
| State | Fully stateless - no server-side sessions |

## Out of Scope

- Password reset or account recovery flows
- Social login or OAuth providers
- Role-based permissions beyond basic user ownership
- Email verification
- Two-factor authentication

---

## Clarifications

### Session 2025-01-06

- Q: How should the frontend store and transmit the JWT token? → A: httpOnly cookie set by Better Auth (most secure, automatic on requests)
- Q: What does "user isolation" mean in terms of implementation layers? → A: Both database (WHERE user_id=X) AND API middleware validation (defense in depth)
- Q: What HTTP status for signup with existing email? → A: 409 Conflict with message "Email already registered"

---

## User Stories

### US-AUTH-001: User Signup (Priority: P1)

**As a** new user
**I want to** create an account with email and password
**So that** I can securely access and manage my personal todo list

**Acceptance Criteria**:

```gherkin
Scenario: Successful signup with valid credentials
  Given I am on the signup page
  When I enter a valid email "user@example.com"
  And I enter a password meeting requirements (min 8 chars)
  And I confirm the password matches
  And I click "Sign Up"
  Then a new user account is created
  And I receive a valid JWT token
  And I am redirected to the dashboard

Scenario: Signup with existing email
  Given a user with email "existing@example.com" exists
  When I attempt to signup with "existing@example.com"
  Then I see an error "Email already registered"
  And no duplicate account is created

Scenario: Signup with weak password
  Given I am on the signup page
  When I enter a password shorter than 8 characters
  Then I see a validation error "Password must be at least 8 characters"
  And the form is not submitted
```

---

### US-AUTH-002: User Signin (Priority: P1)

**As a** registered user
**I want to** sign in with my email and password
**So that** I can access my existing tasks

**Acceptance Criteria**:

```gherkin
Scenario: Successful signin
  Given I have a registered account
  When I enter correct email and password
  And I click "Sign In"
  Then I receive a valid JWT token
  And I am redirected to the dashboard
  And I see only my tasks

Scenario: Signin with wrong password
  Given I have a registered account
  When I enter correct email but wrong password
  Then I see an error "Invalid credentials"
  And no token is issued

Scenario: Signin with non-existent email
  Given no account exists for "unknown@example.com"
  When I attempt to signin with that email
  Then I see an error "Invalid credentials"
  And no token is issued
```

---

### US-AUTH-003: Protected Route Access (Priority: P1)

**As an** authenticated user
**I want** my JWT to grant access to protected resources
**So that** I can perform task operations securely

**Acceptance Criteria**:

```gherkin
Scenario: Access with valid token
  Given I have a valid JWT token
  When I request GET /api/{user_id}/tasks
  And the Authorization header contains "Bearer {token}"
  Then I receive 200 OK
  And I see my tasks

Scenario: Access with expired token
  Given I have an expired JWT token
  When I request any protected endpoint
  Then I receive 401 Unauthorized
  And the response contains "Token expired"

Scenario: Access with invalid token
  Given I have a malformed or tampered JWT
  When I request any protected endpoint
  Then I receive 401 Unauthorized
  And the response contains "Invalid token"

Scenario: Access without token
  Given I have no Authorization header
  When I request any protected endpoint
  Then I receive 401 Unauthorized
  And the response contains "Authentication required"
```

---

### US-AUTH-004: User Isolation (Priority: P1)

**As a** user
**I want** my tasks to be completely isolated from other users
**So that** my data remains private and secure

**Acceptance Criteria**:

```gherkin
Scenario: User can only see own tasks
  Given user A has 3 tasks
  And user B has 5 tasks
  When user A requests their tasks
  Then user A sees exactly 3 tasks
  And none of user B's tasks are visible

Scenario: User cannot access another user's task
  Given user A owns task with ID 1
  When user B attempts to access task ID 1
  Then user B receives 403 Forbidden
  Or user B receives 404 Not Found

Scenario: User ID in URL must match token
  Given I am authenticated as user "abc123"
  When I request GET /api/xyz789/tasks
  Then I receive 403 Forbidden
  And the response contains "Access denied"
```

---

## Technical Specification

### Authentication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION FLOW                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SIGNUP:                                                         │
│  ┌──────────┐    ┌─────────────┐    ┌──────────┐               │
│  │  Client  │───►│ Better Auth │───►│ Database │               │
│  └──────────┘    └─────────────┘    └──────────┘               │
│       │              │                   │                      │
│       │   email,     │   hash password   │   store user        │
│       │   password   │   generate JWT    │   record            │
│       │              │                   │                      │
│       │◄─────────────┤                   │                      │
│       │   JWT token  │                   │                      │
│                                                                  │
│  SIGNIN:                                                         │
│  ┌──────────┐    ┌─────────────┐    ┌──────────┐               │
│  │  Client  │───►│ Better Auth │───►│ Database │               │
│  └──────────┘    └─────────────┘    └──────────┘               │
│       │              │                   │                      │
│       │   email,     │   verify hash     │   lookup user       │
│       │   password   │   generate JWT    │                      │
│       │              │                   │                      │
│       │◄─────────────┤                   │                      │
│       │   JWT token  │                   │                      │
│                                                                  │
│  API ACCESS:                                                     │
│  ┌──────────┐    ┌─────────────┐    ┌──────────┐               │
│  │  Client  │───►│   FastAPI   │───►│ Database │               │
│  └──────────┘    └─────────────┘    └──────────┘               │
│       │              │                   │                      │
│       │   Bearer     │   verify JWT      │   query by          │
│       │   token      │   extract user_id │   user_id           │
│       │              │                   │                      │
│       │◄─────────────┤◄──────────────────┤                      │
│       │   JSON data  │   filtered data   │                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### JWT Token Structure

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_abc123",
    "email": "user@example.com",
    "iat": 1703836800,
    "exp": 1704441600
  },
  "signature": "HMACSHA256(base64(header) + '.' + base64(payload), secret)"
}
```

### Better Auth Configuration (Next.js)

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  database: {
    type: "postgres",
    url: process.env.DATABASE_URL!,
  },
  plugins: [
    jwt({
      secret: process.env.BETTER_AUTH_SECRET!,
      expiresIn: "7d",
    }),
  ],
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
  },
});
```

### FastAPI JWT Verification

```python
# backend/app/dependencies.py
import os
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
SECRET = os.getenv("BETTER_AUTH_SECRET")

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """Verify JWT and return user_id."""
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id",
            )

        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
```

### Environment Variables

```env
# Shared secret for JWT signing/verification
BETTER_AUTH_SECRET=your-256-bit-secret-key-here

# Database connection
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/dbname?sslmode=require
```

---

## Security Considerations

| Concern | Mitigation |
|---------|------------|
| Token theft | HTTPS only, HttpOnly cookies optional |
| Brute force | Rate limiting on auth endpoints |
| Secret exposure | Environment variables, never in code |
| Token replay | Reasonable expiry (7 days) |
| User enumeration | Generic "Invalid credentials" message |

---

## API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/auth/signup` | POST | Create new user account | No |
| `/api/auth/signin` | POST | Authenticate and get token | No |
| `/api/auth/signout` | POST | Invalidate token (client-side) | Yes |
| `/api/auth/session` | GET | Get current session info | Yes |

### Signup Request/Response

**Request**:
```json
POST /api/auth/signup
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Success Response** (201 Created):
```json
{
  "user": {
    "id": "user_abc123",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Error Response** (409 Conflict):
```json
{
  "error": "Email already registered"
}
```

### Signin Request/Response

**Request**:
```json
POST /api/auth/signin
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Success Response** (200 OK):
```json
{
  "user": {
    "id": "user_abc123",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Error Response** (401 Unauthorized):
```json
{
  "error": "Invalid credentials"
}
```

---

## Testing Requirements

### Unit Tests

- [ ] Password hashing produces different hashes for same input (salt)
- [ ] JWT encoding includes all required claims
- [ ] JWT decoding extracts correct user_id
- [ ] Expired tokens are rejected
- [ ] Invalid signatures are rejected

### Integration Tests

- [ ] Signup creates user in database
- [ ] Signin returns valid JWT for correct credentials
- [ ] Protected routes reject requests without token
- [ ] User can only access their own resources

### Security Tests

- [ ] SQL injection attempts are blocked
- [ ] XSS payloads in name field are sanitized
- [ ] Rate limiting triggers after threshold
- [ ] Tokens cannot be forged without secret

---

## Implementation Checklist

- [ ] Configure Better Auth with JWT plugin
- [ ] Set up shared BETTER_AUTH_SECRET
- [ ] Implement signup page and API
- [ ] Implement signin page and API
- [ ] Create FastAPI JWT verification dependency
- [ ] Add auth middleware to all protected routes
- [ ] Implement user_id validation in path params
- [ ] Write comprehensive tests
- [ ] Document API in OpenAPI spec
