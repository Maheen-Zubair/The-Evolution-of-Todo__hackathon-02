# The Evolution of Todo - Phase 2: Full-Stack Web Application

A full-stack todo application with multi-user authentication, built with Next.js 16+ and FastAPI.

## Overview

This is Phase 2 of "The Evolution of Todo" hackathon project, implementing a complete web application with:
- User authentication (signup, signin, signout)
- Personal task management (CRUD operations)
- User isolation (each user only sees their own tasks)
- Responsive, modern UI

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 16+, TypeScript, Tailwind CSS, shadcn/ui |
| Backend | FastAPI, SQLModel, Python 3.11+ |
| Database | Neon PostgreSQL (serverless) |
| Auth | Better Auth (JWT in httpOnly cookies) |
| State | React Query (TanStack Query) |

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- Neon PostgreSQL database

### 1. Clone and setup

```bash
git clone <repo>
cd hackathon-II
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your DATABASE_URL and BETTER_AUTH_SECRET

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

Backend runs at http://localhost:8000

### 3. Frontend setup

```bash
cd frontend
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local with your settings

# Start server
npm run dev
```

Frontend runs at http://localhost:3000

## Project Structure

```
hackathon-II/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI app
│   │   ├── db.py              # Database connection
│   │   ├── dependencies.py    # Auth dependencies
│   │   ├── models/            # SQLModel entities
│   │   └── routers/           # API endpoints
│   ├── migrations/            # Alembic migrations
│   └── tests/                 # pytest tests
├── frontend/                   # Next.js frontend
│   └── src/
│       ├── app/               # App Router pages
│       ├── components/        # React components
│       ├── hooks/             # React Query hooks
│       └── lib/               # Utils, types, API client
└── specs/                      # Design specifications
```

## Features

### Authentication
- Email/password signup with name
- Secure signin with session management
- JWT stored in httpOnly cookies
- Protected routes with automatic redirects

### Task Management
- Create tasks with title and description
- Edit and delete tasks
- Toggle completion status
- Filter by All/Pending/Complete

### User Experience
- Responsive design (mobile, tablet, desktop)
- Optimistic updates for fast feedback
- Loading skeletons
- Inline error messages

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | List user's tasks |
| GET | `/api/tasks/{id}` | Get task by ID |
| POST | `/api/tasks` | Create task |
| PUT | `/api/tasks/{id}` | Full update |
| PATCH | `/api/tasks/{id}` | Partial update |
| DELETE | `/api/tasks/{id}` | Delete task |

All task endpoints require authentication via Better Auth cookies.

## Testing

### Backend tests
```bash
cd backend
pytest
pytest --cov=app  # With coverage
```

### Frontend
```bash
cd frontend
npm run lint
npm run build  # Type checking
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://...@neon.tech/todoapp
BETTER_AUTH_SECRET=<256-bit-secret>
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
```

### Frontend (.env.local)
```
DATABASE_URL=postgresql://...@neon.tech/todoapp
BETTER_AUTH_SECRET=<256-bit-secret>
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Security

- Defense-in-depth user isolation (DB queries + API validation)
- JWT verification on all protected endpoints
- httpOnly cookies prevent XSS token theft
- CORS restricted to frontend URL
- Input validation with Pydantic/Zod

## Related Documentation

- [Frontend README](./frontend/README.md)
- [Backend README](./backend/README.md)
- [API Specification](./specs/api/rest-endpoints.md)
- [Authentication Spec](./specs/features/authentication.md)
- [Implementation Tasks](./specs/002-fullstack-web-app/tasks.md)

## Phase 1 Reference

Phase 1 implemented a CLI todo app in the `001-cli-todo-app` branch. Phase 2 is a fresh implementation sharing only the concept.
