---
title: Phase 2 Implementation Tasks
description: Task list for full-stack web application implementation.
version: "1.0"
status: complete
phase: 2
feature: 002-fullstack-web-app
created: 2025-01-06
updated: 2025-01-07
progress: 76/76 tasks completed (100%)
---

# Tasks: Phase 2 Full-Stack Web Application

**Input**: Design documents from `/specs/002-fullstack-web-app/` and `/specs/features/`, `/specs/api/`, `/specs/database/`, `/specs/ui/`

**Prerequisites**: plan.md (complete), authentication.md, rest-endpoints.md, schema.md, components.md

**Tests**: Integration tests included in Polish phase (E2E testing strategy from plan.md)

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/` (Next.js 16+ App Router)
- **Backend**: `backend/` (FastAPI + SQLModel)
- **Specs**: `specs/` (shared specifications)

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create monorepo structure and initialize both frontend and backend projects

- [x] T001 Create frontend/ and backend/ directory structure
- [x] T002 [P] Initialize Next.js 16+ project with TypeScript in frontend/
- [x] T003 [P] Initialize Python project with FastAPI in backend/
- [x] T004 [P] Create frontend/.env.local with environment template
- [x] T005 [P] Create backend/.env with environment template
- [x] T006 [P] Create backend/requirements.txt with dependencies (fastapi, uvicorn, sqlmodel, python-jose, httpx, python-dotenv, alembic, pytest)
- [x] T007 [P] Configure Tailwind CSS v4 in frontend/
- [x] T008 [P] Install and configure shadcn/ui in frontend/
- [x] T009 [P] Create frontend/lib/types.ts with TypeScript type definitions from data-model.md
- [x] T010 [P] Create frontend/lib/schemas.ts with Zod validation schemas

**Checkpoint**: Both projects initialized, dependencies installed, ready for development

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Database Setup

- [x] T011 Create backend/app/db.py with Neon PostgreSQL connection and session management
- [x] T012 Initialize Alembic for migrations in backend/migrations/
- [x] T013 Create backend/app/models/__init__.py package

### Authentication Infrastructure

- [x] T014 Create frontend/lib/auth.ts with Better Auth configuration
- [x] T015 Create frontend/app/api/auth/[...all]/route.ts for Better Auth API routes
- [x] T016 Create backend/app/dependencies.py with JWT verification dependency (get_current_user)
- [x] T017 Create frontend/lib/auth-client.ts with Better Auth React client

### Backend Core

- [x] T018 Create backend/app/__init__.py package
- [x] T019 Create backend/app/main.py with FastAPI app, CORS config, and router registration
- [x] T020 Create backend/app/routers/__init__.py package

### Frontend Core

- [x] T021 Create frontend/app/layout.tsx with AuthProvider wrapper
- [x] T022 Create frontend/components/providers.tsx with query client and auth providers

**Checkpoint**: Foundation ready - Better Auth configured, JWT verification working, database connected

---

## Phase 3: User Story 1 - User Authentication (Priority: P1) MVP

**Goal**: Users can create accounts and sign in to access the application

**Independent Test**: Navigate to /signup, create account, verify redirect to dashboard; Navigate to /signin, enter credentials, verify JWT cookie set

**User Stories Covered**: US-AUTH-001 (Signup), US-AUTH-002 (Signin)

### Implementation for User Story 1

- [x] T023 [P] [US1] Create frontend/app/(auth)/layout.tsx with centered card layout
- [x] T024 [P] [US1] Create frontend/components/auth/auth-form.tsx with email/password/name fields
- [x] T025 [US1] Create frontend/app/(auth)/signup/page.tsx using AuthForm mode="signup"
- [x] T026 [US1] Create frontend/app/(auth)/signin/page.tsx using AuthForm mode="signin"
- [x] T027 [US1] Add form validation with Zod in auth-form.tsx (min 8 char password)
- [x] T028 [US1] Add loading state (button spinner) during form submission
- [x] T029 [US1] Add inline error display for auth errors (409 duplicate email, 401 invalid credentials)
- [x] T030 [US1] Implement redirect to dashboard after successful auth

**Checkpoint**: User Story 1 complete - users can signup and signin, JWT cookie is set

---

## Phase 4: User Story 2 - Task Management API (Priority: P1)

**Goal**: Authenticated users can perform all CRUD operations on tasks via REST API

**Independent Test**: Use curl/Postman with valid JWT to create, list, update, delete tasks; Verify user isolation

**User Stories Covered**: US-AUTH-003 (Protected Access), US-AUTH-004 (User Isolation)

### Implementation for User Story 2

- [x] T031 [P] [US2] Create backend/app/models/task.py with Task, TaskCreate, TaskUpdate, TaskPatch, TaskRead SQLModel classes
- [x] T032 [US2] Create Alembic migration for task table in backend/migrations/versions/
- [x] T033 [US2] Run migration to create task table with indexes
- [x] T034 [US2] Create backend/app/routers/tasks.py with FastAPI router
- [x] T035 [US2] Implement GET /api/tasks endpoint with filtering (status, limit, offset, sort, order)
- [x] T036 [US2] Implement GET /api/tasks/{task_id} endpoint with ownership check
- [x] T037 [US2] Implement POST /api/tasks endpoint with user_id from JWT
- [x] T038 [US2] Implement PUT /api/tasks/{task_id} endpoint with ownership validation
- [x] T039 [US2] Implement PATCH /api/tasks/{task_id} endpoint for partial updates
- [x] T040 [US2] Implement DELETE /api/tasks/{task_id} endpoint with ownership check
- [x] T041 [US2] Add defense-in-depth: all queries filter by user_id from JWT
- [x] T042 [US2] Register tasks router in backend/app/main.py

**Checkpoint**: User Story 2 complete - all API endpoints working, user isolation enforced, 401/403/404 handled correctly

---

## Phase 5: User Story 3 - Task Dashboard (Priority: P1)

**Goal**: Authenticated users can view their tasks in a responsive dashboard

**Independent Test**: Sign in, navigate to dashboard, see task list with correct count; Filter by status

**Functional Requirements**: TaskList, TaskItem, FilterButtons, EmptyState, Header components

### Implementation for User Story 3

- [x] T043 [P] [US3] Create frontend/lib/api.ts with fetch wrapper for backend API calls
- [x] T044 [P] [US3] Create frontend/hooks/use-tasks.ts with React Query hooks (useTasks, useTask)
- [x] T045 [P] [US3] Create frontend/components/layout/header.tsx with logo and user menu
- [x] T046 [P] [US3] Create frontend/components/layout/user-menu.tsx with signout button
- [x] T047 [US3] Create frontend/app/(dashboard)/layout.tsx with Header and auth protection
- [x] T048 [US3] Create frontend/components/tasks/task-item.tsx with checkbox, title, action buttons
- [x] T049 [US3] Create frontend/components/tasks/task-list.tsx mapping TaskItem components
- [x] T050 [US3] Create frontend/components/tasks/filter-buttons.tsx with All/Pending/Complete toggles
- [x] T051 [US3] Create frontend/components/tasks/empty-state.tsx with contextual messages
- [x] T052 [US3] Create frontend/app/(dashboard)/page.tsx assembling dashboard components
- [x] T053 [US3] Add skeleton loaders for task list loading state
- [x] T054 [US3] Make dashboard responsive (mobile hamburger menu, tablet/desktop full layout)

**Checkpoint**: User Story 3 complete - dashboard shows tasks, filtering works, responsive design verified

---

## Phase 6: User Story 4 - Task Operations UI (Priority: P1)

**Goal**: Users can create, edit, toggle, and delete tasks from the UI

**Independent Test**: Create new task from UI, verify appears in list; Edit task; Toggle completion; Delete with confirmation

**Functional Requirements**: TaskForm, DeleteConfirmDialog, optimistic updates

### Implementation for User Story 4

- [x] T055 [P] [US4] Create frontend/hooks/use-task-mutations.ts with useCreateTask, useUpdateTask, useDeleteTask, useToggleTask
- [x] T056 [P] [US4] Create frontend/components/tasks/task-form.tsx with title/description fields
- [x] T057 [P] [US4] Create frontend/components/tasks/delete-confirm-dialog.tsx with modal
- [x] T058 [US4] Create frontend/app/(dashboard)/tasks/new/page.tsx for task creation
- [x] T059 [US4] Create frontend/app/(dashboard)/tasks/[id]/page.tsx for task editing
- [x] T060 [US4] Wire toggle completion in TaskItem to PATCH endpoint
- [x] T061 [US4] Wire delete button in TaskItem to DELETE endpoint with confirmation
- [x] T062 [US4] Add optimistic updates for toggle and delete operations
- [x] T063 [US4] Add inline error display for failed operations
- [x] T064 [US4] Add character count indicators on TaskForm (500 for title, 2000 for description)

**Checkpoint**: User Story 4 complete - full CRUD from UI working, errors handled gracefully

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final integration, testing, and documentation

### Integration Testing

- [x] T065 [P] Create backend/tests/conftest.py with test fixtures and test database
- [x] T066 [P] Create backend/tests/test_tasks.py with API integration tests
- [x] T067 [P] Create backend/tests/test_auth.py with JWT verification tests
- [x] T068 Write E2E test: user signup → signin → create task → view task → complete task → delete task

### Security & Validation

- [x] T069 Test user isolation: User A cannot access User B's tasks (403/404)
- [x] T070 Test auth failures: missing token (401), invalid token (401), expired token (401)
- [x] T071 Test input validation: empty title rejected, oversized inputs rejected

### Documentation & Cleanup

- [x] T072 [P] Create frontend/README.md with setup instructions
- [x] T073 [P] Create backend/README.md with setup instructions
- [x] T074 [P] Update root README.md with Phase 2 quick start
- [x] T075 Verify OpenAPI docs auto-generated at /docs
- [x] T076 Run accessibility audit (axe-core) and fix critical issues

**Checkpoint**: Phase 2 complete - all tests passing, documentation updated, ready for demo

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundational) ← BLOCKS all user stories
    │
    ├───────────────────────────────────────────┐
    │                                           │
    ▼                                           ▼
Phase 3 (US1: Auth)                    Phase 4 (US2: API)
    │                                           │
    └──────────────┬────────────────────────────┘
                   │
                   ▼
            Phase 5 (US3: Dashboard)
                   │
                   ▼
            Phase 6 (US4: Task Ops UI)
                   │
                   ▼
            Phase 7 (Polish)
```

### User Story Dependencies

| User Story | Depends On | Can Start After |
|------------|------------|-----------------|
| US1 (Auth) | Phase 2 | Foundational complete |
| US2 (API) | Phase 2 | Foundational complete |
| US3 (Dashboard) | US1, US2 | Auth + API working |
| US4 (Task Ops) | US3 | Dashboard visible |

### Within Each User Story

1. Models/schemas before services/hooks
2. Backend before frontend (for API stories)
3. Core components before page assembly
4. Functionality before polish (loading states, errors)

### Parallel Opportunities

**Phase 1 (all parallel):**
```
T002: Init Next.js    T003: Init FastAPI    T004-T010: Config files
```

**Phase 2 (parallel groups):**
```
Group A: T011-T013 (Database)    Group B: T014-T017 (Auth)    Group C: T018-T022 (Core)
```

**US3 + US4 (parallel within stories):**
```
T043: api.ts    T044: use-tasks    T045: header    T046: user-menu
```

---

## Parallel Example: User Story 3

```bash
# Launch all parallel tasks for User Story 3:
Task: "Create frontend/lib/api.ts with fetch wrapper"
Task: "Create frontend/hooks/use-tasks.ts with React Query hooks"
Task: "Create frontend/components/layout/header.tsx"
Task: "Create frontend/components/layout/user-menu.tsx"

# Then sequential:
Task: "Create frontend/app/(dashboard)/layout.tsx"
Task: "Create remaining components..."
```

---

## Implementation Strategy

### MVP First (User Stories 1-2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL)
3. Complete Phase 3: US1 (Auth)
4. Complete Phase 4: US2 (API)
5. **STOP and VALIDATE**: Test API with curl, verify auth works
6. Demo: "Users can signup, signin, and manage tasks via API"

### Full MVP (All User Stories)

1. Setup + Foundational → Foundation ready
2. Add US1 (Auth) → Users can authenticate
3. Add US2 (API) → Full backend working
4. Add US3 (Dashboard) → Users can view tasks
5. Add US4 (Task Ops) → Full CRUD from UI
6. Polish → Tests, docs, accessibility

### Suggested Scope

| Milestone | Stories | Deliverable |
|-----------|---------|-------------|
| Backend MVP | US1 + US2 | Auth + API (curl demo) |
| Frontend MVP | US1 + US3 | Auth + Dashboard (view only) |
| Full MVP | US1-US4 | Complete web app |
| Production | + Polish | Tested, documented |

---

## Task Summary

| Phase | Task Count | Parallel Tasks |
|-------|------------|----------------|
| Phase 1: Setup | 10 | 9 |
| Phase 2: Foundational | 12 | 6 |
| Phase 3: US1 Auth | 8 | 2 |
| Phase 4: US2 API | 12 | 1 |
| Phase 5: US3 Dashboard | 12 | 4 |
| Phase 6: US4 Task Ops | 10 | 3 |
| Phase 7: Polish | 12 | 5 |
| **TOTAL** | **76** | **30** |

---

## Notes

- [P] tasks can run in parallel (different files, no dependencies)
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Use `api-endpoint-generator` skill for API endpoint code
- Use `auth-token-validator` agent for JWT verification logic
