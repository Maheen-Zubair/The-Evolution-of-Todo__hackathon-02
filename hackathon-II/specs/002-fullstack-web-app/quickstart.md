---
title: Phase 2 Quick Start Guide
description: Setup instructions for the full-stack todo web application.
version: "1.0"
status: complete
phase: 2
feature: 002-fullstack-web-app
created: 2025-01-06
updated: 2025-01-06
---

# Phase 2 Quick Start Guide

## Prerequisites

- **Node.js** 20+ (for Next.js frontend)
- **Python** 3.13+ (for FastAPI backend)
- **Neon Account** (free tier: https://neon.tech)
- **Git** (for version control)

---

## 1. Clone & Navigate

```bash
cd hackathon-II
```

---

## 2. Database Setup (Neon)

### 2.1 Create Neon Project

1. Go to https://console.neon.tech
2. Create a new project named "todo-app"
3. Copy the connection string (PostgreSQL URL)

### 2.2 Configure Environment

Create `.env` files in both frontend and backend:

**backend/.env:**
```env
DATABASE_URL=postgresql://user:password@ep-xxx-yyy.us-east-2.aws.neon.tech/todoapp?sslmode=require
BETTER_AUTH_SECRET=your-256-bit-secret-key-generate-with-openssl-rand-base64-32
FRONTEND_URL=http://localhost:3000
```

**frontend/.env.local:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-256-bit-secret-key-same-as-backend
DATABASE_URL=postgresql://user:password@ep-xxx-yyy.us-east-2.aws.neon.tech/todoapp?sslmode=require
```

### 2.3 Generate Secret

```bash
# Generate a secure secret
openssl rand -base64 32
```

---

## 3. Backend Setup (FastAPI)

### 3.1 Create Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3.2 Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
sqlmodel>=0.0.14
psycopg2-binary>=2.9.9
python-jose[cryptography]>=3.3.0
httpx>=0.26.0
python-dotenv>=1.0.0
alembic>=1.13.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
```

### 3.3 Run Database Migrations

```bash
# Initialize Alembic (first time only)
alembic init migrations

# Create initial migration
alembic revision --autogenerate -m "create_task_table"

# Apply migrations
alembic upgrade head
```

### 3.4 Start Backend Server

```bash
uvicorn app.main:app --reload --port 8000
```

**Verify:** http://localhost:8000/docs (OpenAPI documentation)

---

## 4. Frontend Setup (Next.js)

### 4.1 Install Dependencies

```bash
cd frontend
npm install
```

**package.json dependencies:**
```json
{
  "dependencies": {
    "next": "^16.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "better-auth": "^1.0.0",
    "@tanstack/react-query": "^5.0.0",
    "zod": "^3.22.0",
    "react-hook-form": "^7.50.0",
    "@hookform/resolvers": "^3.3.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "@types/react": "^19.0.0",
    "@types/node": "^20.0.0",
    "tailwindcss": "^4.0.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0"
  }
}
```

### 4.2 Initialize shadcn/ui

```bash
npx shadcn@latest init
npx shadcn@latest add button card input label checkbox
```

### 4.3 Start Frontend Server

```bash
npm run dev
```

**Verify:** http://localhost:3000

---

## 5. Verify Setup

### 5.1 Health Check

```bash
# Backend health
curl http://localhost:8000/health

# Frontend
open http://localhost:3000
```

### 5.2 Create Test User

1. Navigate to http://localhost:3000/signup
2. Enter email: test@example.com
3. Enter password: testpassword123
4. Submit form

### 5.3 Test API

```bash
# After signing in (cookie is set), test task creation
# Use browser DevTools to verify cookie is present

# Or test directly with curl (replace with actual cookie value)
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Cookie: better-auth.session_token=YOUR_TOKEN" \
  -d '{"title": "Test task", "description": "Testing API"}'
```

---

## 6. Running Tests

### 6.1 Backend Tests

```bash
cd backend
pytest tests/ -v
```

### 6.2 Frontend Tests

```bash
cd frontend
npm run test        # Unit tests (Vitest)
npm run test:e2e    # E2E tests (Playwright)
```

---

## 7. Project Structure

```
hackathon-II/
├── frontend/                 # Next.js 16+ App Router
│   ├── app/
│   │   ├── (auth)/          # Auth route group
│   │   │   ├── signin/
│   │   │   └── signup/
│   │   ├── (dashboard)/     # Protected routes
│   │   │   ├── page.tsx     # Task list
│   │   │   └── tasks/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── auth/
│   │   ├── layout/
│   │   └── tasks/
│   ├── lib/
│   │   ├── auth-client.ts
│   │   ├── api.ts
│   │   └── types.ts
│   ├── .env.local
│   └── package.json
│
├── backend/                  # FastAPI + SQLModel
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── db.py
│   │   ├── dependencies.py
│   │   ├── models/
│   │   │   └── task.py
│   │   └── routers/
│   │       └── tasks.py
│   ├── tests/
│   │   ├── test_tasks.py
│   │   └── conftest.py
│   ├── migrations/
│   ├── .env
│   └── requirements.txt
│
└── specs/                    # Specifications
    ├── 002-fullstack-web-app/
    │   ├── plan.md
    │   ├── research.md
    │   ├── data-model.md
    │   ├── quickstart.md
    │   └── contracts/
    ├── features/
    ├── api/
    ├── database/
    └── ui/
```

---

## 8. Environment Variables Reference

| Variable | Service | Required | Description |
|----------|---------|----------|-------------|
| DATABASE_URL | Both | Yes | Neon PostgreSQL connection string |
| BETTER_AUTH_SECRET | Both | Yes | Shared JWT signing secret (32+ bytes) |
| FRONTEND_URL | Backend | Yes | Frontend URL for CORS |
| NEXT_PUBLIC_API_URL | Frontend | Yes | Backend API URL |

---

## 9. Common Issues

### Issue: Database connection failed

**Solution:** Verify DATABASE_URL includes `?sslmode=require`

### Issue: CORS errors

**Solution:** Ensure FRONTEND_URL in backend .env matches actual frontend URL

### Issue: JWT verification failed

**Solution:** Ensure BETTER_AUTH_SECRET is identical in both frontend and backend

### Issue: Better Auth tables not created

**Solution:** Better Auth auto-creates tables on first request; ensure database is accessible

---

## 10. Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Run `/sp.implement` to start coding
3. Test each feature as it's implemented
4. Run `/sp.git.commit_pr` when ready to commit

---

## References

- [Better Auth Documentation](https://www.better-auth.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Next.js App Router](https://nextjs.org/docs/app)
- [Neon PostgreSQL](https://neon.tech/docs)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com)
