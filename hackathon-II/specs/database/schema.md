---
title: Database Schema for Persistent Multi-User Todo Storage
description: PostgreSQL database schema design for Neon serverless with SQLModel ORM integration.
version: "1.0"
status: draft
phase: 2
feature: database
created: 2025-12-29
updated: 2025-12-29
authors:
  - Evolution of Todo Team
tags:
  - database
  - postgresql
  - neon
  - sqlmodel
  - schema
dependencies:
  - neon
  - sqlmodel
  - psycopg2
related:
  - specs/features/authentication.md
  - specs/api/rest-endpoints.md
---

# Database Schema for Persistent Multi-User Todo Storage

## Overview

PostgreSQL database schema design for Neon serverless with SQLModel ORM integration.

**Target Audience**: Backend developers implementing database models and migrations

**Focus**: Schema design, indexes, constraints, SQLModel integration, Neon configuration

## Success Criteria

| ID | Criterion | Measurable Outcome |
|----|-----------|-------------------|
| SC-001 | Tasks persist across restarts | Data survives server restart |
| SC-002 | User isolation enforced | Each user sees only their tasks |
| SC-003 | Unique task IDs per user | Auto-incrementing primary key |
| SC-004 | Timestamps auto-managed | created_at/updated_at set automatically |
| SC-005 | Query performance acceptable | p95 < 100ms for common queries |
| SC-006 | Connection pooling works | Handles concurrent requests |
| SC-007 | Foreign key integrity | user_id references valid user |

## Constraints

| Constraint | Requirement |
|------------|-------------|
| Database Provider | Neon Serverless PostgreSQL |
| ORM | SQLModel (Pydantic + SQLAlchemy) |
| Connection | SSL required (sslmode=require) |
| Pool Size | 5-20 connections |
| Max Task Title | 500 characters |
| Max Description | 2000 characters |

## Out of Scope

- Database sharding
- Read replicas
- Full-text search
- Audit logging tables
- Soft delete implementation

---

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    ENTITY RELATIONSHIP DIAGRAM                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────┐         ┌──────────────────────┐     │
│  │        user          │         │        task          │     │
│  ├──────────────────────┤         ├──────────────────────┤     │
│  │ id          VARCHAR  │◄────────┤ user_id     VARCHAR  │     │
│  │ email       VARCHAR  │   1:N   │ id          SERIAL   │     │
│  │ name        VARCHAR  │         │ title       VARCHAR  │     │
│  │ password    VARCHAR  │         │ description TEXT     │     │
│  │ created_at  TIMESTAMP│         │ is_complete BOOLEAN  │     │
│  │ updated_at  TIMESTAMP│         │ created_at  TIMESTAMP│     │
│  └──────────────────────┘         │ updated_at  TIMESTAMP│     │
│                                   └──────────────────────┘     │
│  (Managed by Better Auth)         (Managed by our app)         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tables

### user (Managed by Better Auth)

Better Auth automatically creates and manages the user table. We reference it but don't define it.

```sql
-- Created by Better Auth (do not modify)
CREATE TABLE "user" (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    email_verified BOOLEAN DEFAULT FALSE,
    image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### task (Our Table)

```sql
CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    is_complete BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT task_title_not_empty CHECK (LENGTH(TRIM(title)) > 0),
    CONSTRAINT task_title_max_length CHECK (LENGTH(title) <= 500),
    CONSTRAINT task_description_max_length CHECK (description IS NULL OR LENGTH(description) <= 2000)
);

-- Indexes
CREATE INDEX idx_task_user_id ON task(user_id);
CREATE INDEX idx_task_user_complete ON task(user_id, is_complete);
CREATE INDEX idx_task_user_created ON task(user_id, created_at DESC);
```

---

## SQLModel Definitions

### Task Model

```python
# backend/app/models/task.py
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func

class TaskBase(SQLModel):
    """Base model with shared task properties."""
    title: str = Field(
        min_length=1,
        max_length=500,
        description="Task title"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Optional task description"
    )
    is_complete: bool = Field(
        default=False,
        description="Completion status"
    )

class Task(TaskBase, table=True):
    """Database model for tasks."""
    __tablename__ = "task"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Auto-generated task ID"
    )
    user_id: str = Field(
        index=True,
        foreign_key="user.id",
        description="Owner user ID from Better Auth"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        ),
        description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
        ),
        description="Last update timestamp"
    )

class TaskCreate(TaskBase):
    """Schema for creating a task."""
    pass

class TaskUpdate(TaskBase):
    """Schema for full task update (all fields required)."""
    pass

class TaskPatch(SQLModel):
    """Schema for partial task update (all fields optional)."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_complete: Optional[bool] = None

class TaskRead(TaskBase):
    """Schema for reading a task."""
    id: int
    created_at: datetime
    updated_at: datetime
```

---

## Database Connection

### Neon Configuration

```python
# backend/app/db.py
import os
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import QueuePool

# Connection string from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Neon requires SSL
if DATABASE_URL and "sslmode" not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require"

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set True for SQL logging
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,  # Recycle connections after 30 minutes
)

def get_session():
    """Dependency for FastAPI to get database session."""
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """Create all tables on application startup."""
    SQLModel.metadata.create_all(engine)
```

### Environment Variables

```env
# .env
DATABASE_URL=postgresql://user:password@ep-xxx-yyy.us-east-2.aws.neon.tech/todoapp?sslmode=require
```

---

## Indexes

### Primary Indexes

| Table | Index | Columns | Purpose |
|-------|-------|---------|---------|
| task | pk_task | id | Primary key lookup |
| task | idx_task_user_id | user_id | Filter by user |

### Composite Indexes

| Table | Index | Columns | Purpose |
|-------|-------|---------|---------|
| task | idx_task_user_complete | (user_id, is_complete) | Filter user's complete/pending |
| task | idx_task_user_created | (user_id, created_at DESC) | Sort user's tasks by date |

### Index Usage Examples

```sql
-- Uses idx_task_user_id
SELECT * FROM task WHERE user_id = 'user_abc123';

-- Uses idx_task_user_complete
SELECT * FROM task WHERE user_id = 'user_abc123' AND is_complete = false;

-- Uses idx_task_user_created
SELECT * FROM task WHERE user_id = 'user_abc123' ORDER BY created_at DESC LIMIT 50;
```

---

## Constraints

### Check Constraints

| Constraint | Table | Rule |
|------------|-------|------|
| task_title_not_empty | task | LENGTH(TRIM(title)) > 0 |
| task_title_max_length | task | LENGTH(title) <= 500 |
| task_description_max_length | task | description IS NULL OR LENGTH(description) <= 2000 |

### Foreign Key Constraints

| Constraint | Table | Column | References | On Delete |
|------------|-------|--------|------------|-----------|
| fk_task_user | task | user_id | user(id) | CASCADE |

---

## Migrations

### Initial Migration (Alembic)

```python
# migrations/versions/001_create_task_table.py
"""Create task table

Revision ID: 001
Create Date: 2025-12-29
"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'task',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_complete', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.CheckConstraint("LENGTH(TRIM(title)) > 0", name='task_title_not_empty'),
        sa.CheckConstraint("LENGTH(title) <= 500", name='task_title_max_length'),
        sa.CheckConstraint("description IS NULL OR LENGTH(description) <= 2000", name='task_description_max_length'),
    )

    op.create_index('idx_task_user_id', 'task', ['user_id'])
    op.create_index('idx_task_user_complete', 'task', ['user_id', 'is_complete'])
    op.create_index('idx_task_user_created', 'task', ['user_id', sa.text('created_at DESC')])

def downgrade():
    op.drop_index('idx_task_user_created')
    op.drop_index('idx_task_user_complete')
    op.drop_index('idx_task_user_id')
    op.drop_table('task')
```

---

## Query Patterns

### Common Queries

```python
# List user's tasks with pagination
def get_user_tasks(
    session: Session,
    user_id: str,
    status: str = "all",
    limit: int = 50,
    offset: int = 0
) -> list[Task]:
    query = select(Task).where(Task.user_id == user_id)

    if status == "complete":
        query = query.where(Task.is_complete == True)
    elif status == "pending":
        query = query.where(Task.is_complete == False)

    query = query.order_by(Task.created_at.desc())
    query = query.offset(offset).limit(limit)

    return session.exec(query).all()

# Get single task with ownership check
def get_task_by_id(
    session: Session,
    task_id: int,
    user_id: str
) -> Task | None:
    task = session.get(Task, task_id)
    if task and task.user_id == user_id:
        return task
    return None

# Count user's tasks
def count_user_tasks(session: Session, user_id: str) -> int:
    return session.exec(
        select(func.count()).select_from(Task).where(Task.user_id == user_id)
    ).one()
```

---

## Performance Considerations

### Connection Pooling

```python
# Recommended pool settings for Neon
engine = create_engine(
    DATABASE_URL,
    pool_size=5,          # Base connections
    max_overflow=10,      # Additional connections under load
    pool_timeout=30,      # Wait time for connection
    pool_recycle=1800,    # Refresh connections every 30 min
    pool_pre_ping=True,   # Test connections before use
)
```

### Query Optimization

| Query Pattern | Expected Performance | Index Used |
|--------------|---------------------|------------|
| List user tasks | < 50ms | idx_task_user_created |
| Filter by status | < 50ms | idx_task_user_complete |
| Get single task | < 10ms | pk_task |
| Create task | < 20ms | N/A |
| Update task | < 20ms | pk_task |
| Delete task | < 20ms | pk_task |

---

## Testing Requirements

### Unit Tests

- [ ] Task model validates title constraints
- [ ] Task model validates description constraints
- [ ] TaskCreate schema rejects invalid data
- [ ] TaskPatch schema allows partial data

### Integration Tests

- [ ] Tasks persist after session commit
- [ ] Foreign key constraint prevents orphan tasks
- [ ] Cascade delete removes tasks when user deleted
- [ ] Indexes improve query performance
- [ ] Connection pooling handles concurrent requests

### Migration Tests

- [ ] Upgrade migration creates all tables
- [ ] Downgrade migration removes tables cleanly
- [ ] Migration is idempotent

---

## Implementation Checklist

- [ ] Set up Neon PostgreSQL database
- [ ] Configure DATABASE_URL in environment
- [ ] Create SQLModel Task model
- [ ] Create database session dependency
- [ ] Set up Alembic for migrations
- [ ] Create initial migration
- [ ] Add check constraints
- [ ] Create performance indexes
- [ ] Configure connection pooling
- [ ] Write database integration tests
- [ ] Document backup/restore procedures
