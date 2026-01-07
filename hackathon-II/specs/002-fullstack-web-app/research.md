---
title: Phase 2 Research & Technology Decisions
description: Research findings and technology decisions for the full-stack web application.
version: "1.0"
status: complete
phase: 2
feature: 002-fullstack-web-app
created: 2025-01-06
updated: 2025-01-06
---

# Phase 2 Research & Technology Decisions

## Overview

This document consolidates all research findings and technology decisions for Phase 2: Full-Stack Web Application. All decisions are traced to clarification sessions and spec requirements.

---

## 1. Authentication Strategy

### Decision: Better Auth with JWT in httpOnly Cookies

**Rationale:**
- httpOnly cookies prevent XSS attacks from stealing tokens
- Automatic transmission on requests simplifies frontend code
- Better Auth provides built-in Next.js integration
- Shared `BETTER_AUTH_SECRET` enables stateless verification in FastAPI

**Alternatives Considered:**
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| localStorage + Authorization header | Simple implementation | XSS vulnerable, manual header management | Security risk |
| In-memory + refresh token | Most secure | Complex implementation, requires refresh flow | Over-engineered for todo app |
| Session-based auth | Simple, server-controlled | Requires session storage, not stateless | Violates stateless requirement |

**Source:** Clarification Session 2025-01-06, Q1

---

## 2. User Isolation Strategy

### Decision: Defense-in-Depth (Database + API layers)

**Rationale:**
- Database-level: All queries include `WHERE user_id = ?` clause
- API-level: Middleware validates ownership before any operation
- Double protection prevents data leaks even if one layer has bugs
- Industry best practice for multi-tenant applications

**Alternatives Considered:**
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Database only | Simpler code | Single point of failure | Security risk |
| API only | Centralized logic | Queries could bypass middleware | Security risk |
| Row-level security (PostgreSQL RLS) | Database-enforced | Added complexity, Neon support unclear | Unnecessary complexity |

**Source:** Clarification Session 2025-01-06, Q2

---

## 3. Error Response Strategy

### Decision: 409 Conflict for Duplicate Email

**Rationale:**
- Semantically correct HTTP status for "resource already exists"
- Clear differentiation from validation errors (422) and bad requests (400)
- Client can programmatically detect duplicate email vs other errors

**HTTP Status Code Mapping:**
| Scenario | Status | Message |
|----------|--------|---------|
| Duplicate email signup | 409 Conflict | "Email already registered" |
| Invalid credentials (signin) | 401 Unauthorized | "Invalid credentials" |
| Missing/invalid JWT | 401 Unauthorized | "Not authenticated" |
| Cross-user access | 403 Forbidden | "Access denied" |
| Resource not found | 404 Not Found | "{Resource} not found" |
| Validation failure | 422 Unprocessable | Pydantic error details |

**Source:** Clarification Session 2025-01-06, Q3

---

## 4. UI Feedback Strategy

### Decision: Inline Feedback Pattern

**Rationale:**
- Skeleton loaders for lists feel faster than spinners
- Button spinners indicate action in progress without blocking UI
- Inline error messages keep context (no disruptive modals)
- Consistent with modern SaaS UX patterns

**Implementation:**
| Context | Loading State | Error State |
|---------|---------------|-------------|
| Task list | Skeleton cards | Inline error banner |
| Form submission | Button spinner + disabled | Red text below field |
| Toggle/Delete | Optimistic update | Revert + inline error |
| Page load | Full skeleton layout | Error boundary |

**Alternatives Considered:**
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Toast notifications | Non-intrusive | Can be missed, no context | Less discoverable |
| Modal dialogs | Attention-grabbing | Disruptive UX | Over-intrusive |
| Full-screen loaders | Clear loading state | Blocks all interaction | Poor UX |

**Source:** Clarification Session 2025-01-06, Q4

---

## 5. Code Reuse Strategy

### Decision: Fresh Implementation (Phase 1 as Reference Only)

**Rationale:**
- Phase 2 has fundamentally different architecture (web vs CLI)
- Different storage (PostgreSQL vs in-memory dict)
- Different user model (multi-user vs single-user)
- Clean separation prevents technical debt
- Phase 1 business logic can inform but not constrain Phase 2

**What to Reference from Phase 1:**
- Task field names and validation rules
- CRUD operation semantics
- Test scenarios and edge cases

**What NOT to Reuse:**
- Task dataclass (incompatible with SQLModel)
- TaskManager class (different storage paradigm)
- CLI interface code

**Source:** Clarification Session 2025-01-06, Q5

---

## 6. Monorepo Structure

### Decision: Separate frontend/ and backend/ Folders

**Rationale:**
- Clear separation of concerns
- Independent deployment possible
- Separate dependency management (npm vs pip)
- Easier CI/CD pipeline configuration
- Standard industry practice

**Structure:**
```
hackathon-II/
├── frontend/           # Next.js 16+ App Router
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── package.json
├── backend/            # FastAPI + SQLModel
│   ├── app/
│   ├── tests/
│   └── requirements.txt
└── specs/              # Shared specifications
```

**Source:** User input for /sp.plan command

---

## 7. Database Choice

### Decision: Neon Serverless PostgreSQL with SQLModel ORM

**Rationale:**
- Serverless: No server management, auto-scaling
- Free tier: Suitable for hackathon/development
- PostgreSQL: Industry-standard, robust feature set
- SQLModel: Combines Pydantic validation with SQLAlchemy ORM
- SSL required: Security by default

**Connection Configuration:**
- Pool size: 5 base connections
- Max overflow: 10 additional under load
- Pool recycle: 1800 seconds (30 minutes)
- SSL mode: require

**Source:** Constitution Phase II rules, specs/database/schema.md

---

## 8. Frontend Framework

### Decision: Next.js 16+ with App Router

**Rationale:**
- App Router: Modern React patterns (RSC, Suspense)
- TypeScript: Type safety reduces runtime errors
- Tailwind CSS v4: Utility-first, rapid iteration
- shadcn/ui: Accessible, customizable components
- Better Auth integration: Official React hooks

**Key Patterns:**
- Server Components for data fetching
- Client Components for interactivity
- Route groups for layout organization
- Server Actions for mutations (optional)

**Source:** Constitution Phase II rules, specs/ui/components.md

---

## 9. API Design

### Decision: RESTful API with OpenAPI Documentation

**Rationale:**
- REST: Simple, well-understood, HTTP-native
- OpenAPI: Auto-generated documentation, client generation
- FastAPI: Built-in async, automatic OpenAPI generation
- Versioning: Not needed for v1, prepare for future

**Phase 3 Extensibility:**
- API structure supports chatbot tool calls
- Endpoints map 1:1 to MCP tools
- Stateless design enables AI agent integration

**Source:** Constitution Phase III preview, specs/api/rest-endpoints.md

---

## 10. Testing Strategy

### Decision: Multi-Layer Testing Approach

**Rationale:**
- Unit tests: Fast feedback on component logic
- Integration tests: Verify API + DB interaction
- E2E tests: Validate user journeys
- Security tests: Verify auth and isolation

**Testing Tools:**
| Layer | Backend | Frontend |
|-------|---------|----------|
| Unit | pytest | Vitest |
| Integration | pytest + TestClient | Playwright |
| E2E | pytest (API) | Playwright |
| Security | pytest + custom | Playwright |

**Source:** Constitution Principle VI (Testing)

---

## Unresolved Items (Deferred to Implementation)

| Item | Reason for Deferral | Resolution Timing |
|------|---------------------|-------------------|
| Rate limiting implementation | Implementation detail | During API endpoint coding |
| Concurrent edit handling | Low priority for v1 | Post-MVP if needed |
| Exact environment variable list | Depends on deployment | During setup phase |

---

## References

- specs/features/authentication.md
- specs/api/rest-endpoints.md
- specs/database/schema.md
- specs/ui/components.md
- specs/overview.md
- .specify/memory/constitution.md
