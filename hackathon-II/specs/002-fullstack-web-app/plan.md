---
title: Phase 2 Implementation Plan
description: Full-stack web application implementation plan for multi-user todo app.
version: "1.0"
status: complete
phase: 2
feature: 002-fullstack-web-app
created: 2025-01-06
updated: 2025-01-06
authors:
  - Evolution of Todo Team
---

# Phase 2 Implementation Plan

## Executive Summary

Transform the Phase 1 CLI Todo App into a multi-user full-stack web application with persistent storage, JWT authentication, and responsive UI.

**Timeline:** Implementation organized in 5 sequential phases
**Approach:** Fresh implementation with Phase 1 as reference only
**Key Technologies:** Next.js 16+, FastAPI, Neon PostgreSQL, Better Auth

---

## Technical Context

### Technology Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| Frontend | Next.js | 16+ | App Router, RSC, TypeScript |
| UI Components | shadcn/ui | Latest | Accessible, customizable |
| Styling | Tailwind CSS | 4.0 | Utility-first CSS |
| Backend | FastAPI | 0.109+ | Async REST API |
| ORM | SQLModel | 0.0.14+ | Pydantic + SQLAlchemy |
| Database | Neon PostgreSQL | Serverless | Persistent storage |
| Auth | Better Auth | 1.0+ | JWT in httpOnly cookies |
| Testing | pytest, Vitest, Playwright | Latest | Multi-layer testing |

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PHASE 2 ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐          ┌─────────────────┐          ┌─────────────┐ │
│  │     Browser     │          │     Next.js     │          │   FastAPI   │ │
│  │                 │  HTTP    │    Frontend     │   HTTP   │   Backend   │ │
│  │  React 19 SPA   │◄────────►│   (Port 3000)   │◄────────►│ (Port 8000) │ │
│  └─────────────────┘          └─────────────────┘          └─────────────┘ │
│          │                           │                           │          │
│          │ httpOnly                  │ Better Auth               │ SQLModel │
│          │ Cookie                    │ (JWT signing)             │ ORM      │
│          │                           │                           │          │
│          │                    ┌──────┴──────┐             ┌──────┴──────┐  │
│          │                    │ Session DB  │             │    Neon     │  │
│          └───────────────────►│ (user, etc) │             │ PostgreSQL  │  │
│                               └─────────────┘             └─────────────┘  │
│                                                                              │
│  Shared: BETTER_AUTH_SECRET for JWT verification                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Auth Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            AUTHENTICATION FLOW                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  SIGNUP/SIGNIN:                                                              │
│  ┌─────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │ Browser │───►│ Next.js     │───►│ Better Auth │───►│ Neon PostgreSQL │  │
│  │         │    │ /api/auth/* │    │ (validate)  │    │ (store user)    │  │
│  └─────────┘    └─────────────┘    └─────────────┘    └─────────────────┘  │
│       ▲                │                                                     │
│       │                │ Set-Cookie: httpOnly JWT                           │
│       └────────────────┘                                                     │
│                                                                              │
│  API REQUEST:                                                                │
│  ┌─────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │ Browser │───►│ Next.js     │───►│   FastAPI   │───►│ Neon PostgreSQL │  │
│  │ + Cookie│    │ (pass thru) │    │ (verify JWT)│    │ (query tasks)   │  │
│  └─────────┘    └─────────────┘    └─────────────┘    └─────────────────┘  │
│       ▲                                   │                                  │
│       │                                   │ Extract user_id from JWT        │
│       │                                   │ Filter: WHERE user_id = ?       │
│       └───────────────────────────────────┘                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Constitution Check

### Principle Compliance

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Accuracy | PASS | Implementation follows specs exactly |
| II. Clarity | PASS | Clear naming, documented decisions |
| III. Reproducibility | PASS | Deterministic builds, locked deps |
| IV. Rigor | PASS | Industry patterns (REST, JWT, ORM) |
| V. Security | PASS | JWT httpOnly, defense-in-depth |
| VI. Testing | PASS | Unit + integration + E2E planned |
| VII. Documentation | PASS | OpenAPI, quickstart, README |

### Phase II Rule Compliance

| Rule | Status | Implementation |
|------|--------|----------------|
| RESTful API endpoints | PASS | /api/tasks CRUD endpoints |
| JWT-based auth (Better Auth) | PASS | httpOnly cookies, shared secret |
| Database: Neon PostgreSQL | PASS | SQLModel ORM integration |
| ORM: SQLModel | PASS | Pydantic + SQLAlchemy |
| Responsive UI (Next.js + Tailwind) | PASS | Mobile-first, breakpoints defined |

---

## Key Decisions (Requiring ADR Consideration)

### Decision 1: JWT Storage in httpOnly Cookies

**Options Considered:**
1. httpOnly cookie (chosen)
2. localStorage + Authorization header
3. In-memory + refresh token

**Tradeoffs:**
| Factor | httpOnly Cookie | localStorage |
|--------|-----------------|--------------|
| XSS Protection | High | None |
| CSRF Risk | Medium (mitigate with SameSite) | None |
| Implementation | Simple (auto-send) | Manual header |
| Cross-domain | Requires CORS setup | Flexible |

**Decision:** httpOnly cookie for security-first approach
**ADR:** Consider documenting if project requires cross-domain API

### Decision 2: Defense-in-Depth User Isolation

**Options Considered:**
1. Database + API (chosen)
2. Database only
3. API only

**Tradeoffs:**
| Factor | Both Layers | Single Layer |
|--------|-------------|--------------|
| Security | High (redundant) | Lower |
| Complexity | Higher | Lower |
| Performance | Negligible diff | Slightly better |
| Debugging | More verbose | Simpler |

**Decision:** Both layers for maximum security
**ADR:** Not required (standard best practice)

### Decision 3: Fresh Implementation (No Phase 1 Reuse)

**Options Considered:**
1. Fresh implementation (chosen)
2. Shared core library
3. Migrate data structures

**Rationale:**
- Different architectures (web vs CLI)
- Different storage paradigms
- Different user models
- Clean separation prevents debt

**ADR:** Not required (architectural evolution)

---

## Implementation Phases

### Phase A: Project Setup & Auth (Foundation)

**Objective:** Set up monorepo, configure auth, verify end-to-end flow

**Tasks:**
1. Create frontend/ and backend/ directories
2. Initialize Next.js 16+ with TypeScript
3. Initialize FastAPI with SQLModel
4. Configure Neon PostgreSQL connection
5. Set up Better Auth in Next.js
6. Implement JWT verification in FastAPI
7. Create signin/signup pages
8. Test auth flow end-to-end

**Deliverables:**
- Working auth flow (signup → signin → protected route)
- Environment configuration documented
- Basic project structure

**Success Criteria:**
- User can create account
- User can sign in
- JWT cookie is set (httpOnly)
- FastAPI can verify JWT and extract user_id

---

### Phase B: Database & Models

**Objective:** Set up database schema and ORM models

**Tasks:**
1. Create SQLModel Task model
2. Set up Alembic migrations
3. Run initial migration
4. Create TaskCreate, TaskUpdate, TaskPatch, TaskRead schemas
5. Test database CRUD operations
6. Create TypeScript types for frontend

**Deliverables:**
- Task table in Neon
- SQLModel models
- Alembic migration files
- TypeScript type definitions

**Success Criteria:**
- Tasks table created with all columns
- Indexes created for performance
- Foreign key to user table works
- CRUD operations work in isolation

---

### Phase C: API Endpoints

**Objective:** Implement all REST API endpoints

**Tasks:**
1. Create FastAPI router for /api/tasks
2. Implement GET /api/tasks (list with filtering)
3. Implement GET /api/tasks/{id}
4. Implement POST /api/tasks
5. Implement PUT /api/tasks/{id}
6. Implement PATCH /api/tasks/{id}
7. Implement DELETE /api/tasks/{id}
8. Add user_id filtering (defense-in-depth)
9. Add ownership validation
10. Write API integration tests

**Reusable Intelligence:**
- Use `api-endpoint-generator` skill for code generation
- Use `auth-token-validator` agent for JWT logic

**Deliverables:**
- All 6 API endpoints working
- OpenAPI documentation auto-generated
- Integration tests passing

**Success Criteria:**
- All endpoints return correct status codes
- User isolation enforced
- Invalid tokens rejected with 401
- Cross-user access returns 403

---

### Phase D: Frontend Pages & Components

**Objective:** Build all UI components and pages

**Tasks:**
1. Create AuthForm component (signin/signup modes)
2. Create Header component with UserMenu
3. Create TaskList component
4. Create TaskItem component
5. Create TaskForm component (create/edit)
6. Create FilterButtons component
7. Create EmptyState component
8. Create DeleteConfirmDialog component
9. Implement dashboard page
10. Implement task create/edit pages
11. Add skeleton loaders
12. Add inline error display
13. Make responsive (mobile-first)

**Deliverables:**
- All pages functional
- Components reusable
- Responsive design verified

**Success Criteria:**
- Users can perform all CRUD operations
- Loading states visible
- Errors displayed inline
- Works on mobile/tablet/desktop

---

### Phase E: Integration & Testing

**Objective:** Full integration testing and polish

**Tasks:**
1. Write E2E tests (Playwright)
2. Test user isolation scenarios
3. Test auth failure scenarios
4. Test form validation
5. Accessibility audit (axe-core)
6. Performance audit (Lighthouse)
7. Fix any issues found
8. Update documentation

**Deliverables:**
- All tests passing
- Accessibility compliant
- Performance acceptable
- Documentation complete

**Success Criteria:**
- E2E tests cover all user journeys
- WCAG AA compliance
- LCP < 2.5s on 3G
- All specs satisfied

---

## Testing Strategy

### Test Pyramid

```
        ┌─────────┐
        │   E2E   │  Playwright (5-10 tests)
        │  Tests  │  - Full user journeys
        └────┬────┘
             │
      ┌──────┴──────┐
      │ Integration │  pytest + TestClient (20-30 tests)
      │    Tests    │  - API + DB interaction
      └──────┬──────┘
             │
    ┌────────┴────────┐
    │   Unit Tests    │  pytest + Vitest (50+ tests)
    │                 │  - Models, schemas, components
    └─────────────────┘
```

### Test Coverage by Spec

| Spec | Test Type | Key Scenarios |
|------|-----------|---------------|
| authentication.md | Integration | Signup, signin, token validation |
| rest-endpoints.md | Integration | CRUD operations, error codes |
| schema.md | Unit | Model validation, constraints |
| components.md | Unit + E2E | Rendering, interactions |

### Security Test Cases

1. **Token Tests:**
   - Missing token → 401
   - Invalid token → 401
   - Expired token → 401

2. **Isolation Tests:**
   - User A cannot see User B's tasks
   - User A cannot modify User B's tasks
   - User A cannot delete User B's tasks

3. **Input Tests:**
   - SQL injection blocked
   - XSS payloads sanitized
   - Oversized inputs rejected

---

## Phase 3 Extensibility

The API design prepares for Phase 3 (AI Chatbot) by:

1. **MCP Tool Mapping:**
   | API Endpoint | MCP Tool |
   |--------------|----------|
   | POST /api/tasks | add_task |
   | GET /api/tasks | list_tasks |
   | PATCH /api/tasks/{id} | complete_task / update_task |
   | DELETE /api/tasks/{id} | delete_task |

2. **Stateless Design:**
   - No server-side sessions
   - JWT contains all needed user info
   - Each request independent

3. **Consistent Response Format:**
   - Standard JSON structure
   - Predictable error messages
   - Machine-parseable for AI

---

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Neon cold start latency | Medium | Low | Connection pooling, keep-alive |
| Better Auth breaking changes | Low | Medium | Pin dependency version |
| JWT secret exposure | Low | High | Environment variables only |
| CORS issues | Medium | Low | Configure properly upfront |

---

## Artifacts Generated

| Artifact | Path | Description |
|----------|------|-------------|
| Implementation Plan | specs/002-fullstack-web-app/plan.md | This document |
| Research Decisions | specs/002-fullstack-web-app/research.md | Technology choices |
| Data Model | specs/002-fullstack-web-app/data-model.md | Entity definitions |
| API Contract | specs/002-fullstack-web-app/contracts/openapi.yaml | OpenAPI spec |
| Quick Start | specs/002-fullstack-web-app/quickstart.md | Setup guide |

---

## Next Steps

1. Run `/sp.tasks` to generate implementation task list
2. Run `/sp.implement` to begin coding
3. Follow phase order: A → B → C → D → E
4. Use existing skills for code generation
5. Create PHRs after each implementation session

---

## References

- specs/features/authentication.md
- specs/api/rest-endpoints.md
- specs/database/schema.md
- specs/ui/components.md
- specs/overview.md
- .specify/memory/constitution.md
- .claude/skills/api-endpoint-generator/SKILL.md
- .claude/agents/auth-token-validator/AGENT.md
