# Phase 2 Todo App - Backend

FastAPI REST API with SQLModel ORM and Neon PostgreSQL.

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Database**: Neon PostgreSQL (serverless)
- **Migrations**: Alembic
- **Auth**: JWT verification via Better Auth
- **Testing**: pytest

## Prerequisites

- Python 3.11+
- Neon PostgreSQL database
- Better Auth configured on frontend

## Setup

1. **Create virtual environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env`:
   ```
   DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/todoapp?sslmode=require
   BETTER_AUTH_SECRET=your-256-bit-secret
   FRONTEND_URL=http://localhost:3000
   ENVIRONMENT=development
   ```

4. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

5. **Start development server**:
   ```bash
   uvicorn app.main:app --reload
   ```

   API available at [http://localhost:8000](http://localhost:8000)
   OpenAPI docs at [http://localhost:8000/docs](http://localhost:8000/docs)

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI application
│   ├── db.py               # Database connection
│   ├── dependencies.py     # Auth dependencies
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py         # Task SQLModel
│   └── routers/
│       ├── __init__.py
│       └── tasks.py        # Task API endpoints
├── migrations/
│   ├── env.py              # Alembic config
│   └── versions/           # Migration files
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Test fixtures
│   ├── test_tasks.py       # Task API tests
│   └── test_auth.py        # Auth tests
├── .env                    # Environment variables
├── alembic.ini             # Alembic configuration
└── requirements.txt        # Python dependencies
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | List user's tasks |
| GET | `/api/tasks/{id}` | Get task by ID |
| POST | `/api/tasks` | Create task |
| PUT | `/api/tasks/{id}` | Full update |
| PATCH | `/api/tasks/{id}` | Partial update |
| DELETE | `/api/tasks/{id}` | Delete task |

### Query Parameters (GET /api/tasks)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `status` | string | `all` | Filter: `all`, `complete`, `pending` |
| `limit` | int | 50 | Max results (1-100) |
| `offset` | int | 0 | Pagination offset |
| `sort` | string | `created_at` | Sort field |
| `order` | string | `desc` | Sort order |

## Authentication

All `/api/tasks` endpoints require authentication via Better Auth cookies:

```
Cookie: better-auth.session_token=<jwt>
```

The JWT is verified using the shared `BETTER_AUTH_SECRET`.

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_tasks.py

# Run with verbose output
pytest -v
```

## Scripts

| Command | Description |
|---------|-------------|
| `uvicorn app.main:app --reload` | Development server |
| `alembic upgrade head` | Run migrations |
| `alembic revision --autogenerate -m "message"` | Generate migration |
| `pytest` | Run tests |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | Neon PostgreSQL connection string |
| `BETTER_AUTH_SECRET` | Yes | Secret for JWT verification |
| `FRONTEND_URL` | Yes | Frontend URL for CORS |
| `ENVIRONMENT` | No | `development` or `production` |

## Security

- All task queries filter by `user_id` from JWT (defense in depth)
- Ownership validated before any modification
- CORS restricted to frontend URL
- No sensitive data in responses
