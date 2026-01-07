---
title: The Evolution of Todo - Project Overview
description: Complete project overview spanning Phase 1 CLI app to Phase 2 full-stack web application.
version: "2.0"
status: active
created: 2025-12-29
updated: 2025-12-29
authors:
  - Evolution of Todo Team
tags:
  - overview
  - roadmap
  - architecture
  - evolution
---

# The Evolution of Todo - Project Overview

## Project Vision

Demonstrate the natural evolution of a software application from a simple CLI tool to a production-ready full-stack web application, showcasing spec-driven development practices at each phase.

---

## Phase Summary

| Phase | Name | Status | Description |
|-------|------|--------|-------------|
| 1 | CLI Todo App | Complete | Single-user, in-memory, Python CLI |
| 2 | Full-Stack Web App | In Progress | Multi-user, persistent, Next.js + FastAPI |
| 3 | Advanced Features | Planned | Real-time, offline support, mobile |

---

## Phase 1: CLI Todo App (Complete)

### Overview

A command-line todo application built with Python 3.13+ using only the standard library. Demonstrates core CRUD operations with in-memory storage.

### Key Features

- Menu-driven CLI interface
- In-memory task storage (dict-based)
- CRUD operations (Create, Read, Update, Delete)
- Toggle task completion
- Input validation and error handling

### Technical Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.13+ |
| Storage | In-memory dictionary |
| Testing | pytest |
| Dependencies | Standard library only |

### Artifacts

- `specs/001-cli-todo-app/spec.md` - Feature specification
- `specs/001-cli-todo-app/plan.md` - Implementation plan
- `specs/001-cli-todo-app/tasks.md` - Development tasks
- `src/task.py` - Task dataclass
- `src/task_manager.py` - TaskManager with CRUD
- `src/main.py` - CLI interface

### Metrics

- 46 tests passing
- 100% core functionality coverage
- O(1) task lookup performance

---

## Phase 2: Full-Stack Web Application (Current)

### Overview

Transform the CLI app into a multi-user web application with persistent storage, authentication, and a responsive UI. Users can access their tasks from any device.

### Key Features

- User authentication (signup, signin, signout)
- JWT-based stateless authentication
- Persistent PostgreSQL storage
- RESTful API for task operations
- Responsive web interface
- User data isolation

### Technical Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Next.js 16+, TypeScript, Tailwind CSS |
| Backend | FastAPI, SQLModel, Python 3.13+ |
| Database | Neon Serverless PostgreSQL |
| Auth | Better Auth with JWT plugin |
| API | REST with OpenAPI documentation |

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 2 ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Browser    │    │   Next.js    │    │   FastAPI    │      │
│  │   (React)    │◄──►│   Frontend   │◄──►│   Backend    │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                   │                   │               │
│         │                   │                   │               │
│         │            ┌──────────────┐    ┌──────────────┐      │
│         │            │  Better Auth │    │     Neon     │      │
│         └───────────►│  (JWT Auth)  │    │  PostgreSQL  │      │
│                      └──────────────┘    └──────────────┘      │
│                             │                   │               │
│                             └───────────────────┘               │
│                            Shared BETTER_AUTH_SECRET            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Specification Documents

| Document | Path | Description |
|----------|------|-------------|
| Authentication | `specs/features/authentication.md` | JWT auth with Better Auth |
| REST API | `specs/api/rest-endpoints.md` | Task CRUD endpoints |
| Database | `specs/database/schema.md` | PostgreSQL schema design |
| UI Components | `specs/ui/components.md` | React component architecture |

### Success Criteria

| ID | Criterion | Target |
|----|-----------|--------|
| SC-001 | User registration works | 100% |
| SC-002 | User login works | 100% |
| SC-003 | Tasks persist across sessions | 100% |
| SC-004 | User isolation enforced | 100% |
| SC-005 | API response time | p95 < 200ms |
| SC-006 | UI responsive | Mobile-first |
| SC-007 | Accessibility | WCAG AA |

---

## Phase 3: Advanced Features (Planned)

### Overview

Enhance the web application with advanced features for power users and improved user experience.

### Planned Features

- Real-time updates (WebSocket)
- Offline support (PWA)
- Task due dates and reminders
- Task categories and tags
- Dark mode
- Mobile app (React Native)
- Task sharing and collaboration

### Technical Considerations

| Feature | Technology Options |
|---------|-------------------|
| Real-time | WebSocket, Server-Sent Events |
| Offline | Service Workers, IndexedDB |
| Mobile | React Native, Expo |
| Push Notifications | Web Push API, FCM |

---

## Project Structure

```
hackathon-II/
├── specs/                          # Specifications
│   ├── overview.md                 # This file
│   ├── 001-cli-todo-app/          # Phase 1 specs
│   │   ├── spec.md
│   │   ├── plan.md
│   │   └── tasks.md
│   ├── features/                   # Phase 2 feature specs
│   │   └── authentication.md
│   ├── api/                        # Phase 2 API specs
│   │   └── rest-endpoints.md
│   ├── database/                   # Phase 2 database specs
│   │   └── schema.md
│   └── ui/                         # Phase 2 UI specs
│       └── components.md
│
├── src/                            # Phase 1 source code
│   ├── task.py
│   ├── task_manager.py
│   └── main.py
│
├── tests/                          # Phase 1 tests
│   ├── test_task.py
│   ├── test_task_manager.py
│   └── test_main.py
│
├── frontend/                       # Phase 2 Next.js app (TBD)
│   ├── app/
│   ├── components/
│   └── lib/
│
├── backend/                        # Phase 2 FastAPI app (TBD)
│   ├── app/
│   │   ├── routers/
│   │   ├── models/
│   │   └── dependencies.py
│   └── tests/
│
├── .claude/                        # Claude Code configuration
│   ├── skills/                     # Reusable skills
│   │   └── api-endpoint-generator/
│   └── agents/                     # Autonomous agents
│       └── auth-token-validator/
│
├── history/                        # Development history
│   └── prompts/                    # Prompt History Records
│
└── .specify/                       # Spec-Kit Plus configuration
    ├── memory/
    │   └── constitution.md
    └── templates/
```

---

## Development Workflow

### Spec-Driven Development (SDD)

1. **Specify** - Define requirements in spec.md
2. **Plan** - Design architecture in plan.md
3. **Task** - Break down into tasks.md
4. **Implement** - Red-Green-Refactor cycle
5. **Document** - PHR and ADR records

### Branching Strategy

| Branch | Purpose |
|--------|---------|
| main | Production-ready code |
| 001-cli-todo-app | Phase 1 feature branch |
| 002-web-app | Phase 2 feature branch |
| feature/* | Individual features |

---

## Clarifications

### Session 2025-01-06

- Q: Phase 1 to Phase 2 code relationship? → A: Fresh implementation, Phase 1 as reference only (clean separation, no shared code)

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Frontend Framework | Next.js 16+ | App Router, RSC, excellent DX |
| Backend Framework | FastAPI | Async, auto-docs, type safety |
| Database | Neon PostgreSQL | Serverless, scalable, free tier |
| Auth Library | Better Auth | Simple JWT, Next.js integration |
| ORM | SQLModel | Pydantic + SQLAlchemy, type safe |
| Styling | Tailwind CSS | Utility-first, fast iteration |
| Phase Migration | Fresh implementation | Phase 1 CLI as reference only, no shared code |

---

## Getting Started

### Phase 1 (CLI)

```bash
# Run the CLI app
cd hackathon-II
python src/main.py

# Run tests
pytest tests/ -v
```

### Phase 2 (Web App)

```bash
# Backend (FastAPI)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (Next.js)
cd frontend
npm install
npm run dev
```

---

## Related Documents

- [Project Constitution](/.specify/memory/constitution.md)
- [Phase 1 Specification](/specs/001-cli-todo-app/spec.md)
- [Authentication Spec](/specs/features/authentication.md)
- [REST API Spec](/specs/api/rest-endpoints.md)
- [Database Schema](/specs/database/schema.md)
- [UI Components](/specs/ui/components.md)
