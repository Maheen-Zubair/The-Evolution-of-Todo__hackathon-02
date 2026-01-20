---
title: Phase 2 Data Model Specification
description: Entity definitions, relationships, and validation rules for the full-stack web application.
version: "1.0"
status: complete
phase: 2
feature: 002-fullstack-web-app
created: 2025-01-06
updated: 2025-01-06
---

# Phase 2 Data Model Specification

## Overview

This document defines all entities, their attributes, relationships, and validation rules for Phase 2: Full-Stack Web Application.

---

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ENTITY RELATIONSHIPS                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌─────────────────────┐                 ┌─────────────────────┐       │
│   │        User         │                 │        Task         │       │
│   │  (Better Auth)      │                 │    (Our Entity)     │       │
│   ├─────────────────────┤                 ├─────────────────────┤       │
│   │ id: VARCHAR(255) PK │◄───────────────►│ id: SERIAL PK       │       │
│   │ email: VARCHAR(255) │      1:N        │ user_id: VARCHAR FK │       │
│   │ name: VARCHAR(255)  │                 │ title: VARCHAR(500) │       │
│   │ email_verified: BOOL│                 │ description: TEXT   │       │
│   │ image: TEXT         │                 │ is_complete: BOOL   │       │
│   │ created_at: TIMESTAMP                 │ created_at: TIMESTAMP       │
│   │ updated_at: TIMESTAMP                 │ updated_at: TIMESTAMP       │
│   └─────────────────────┘                 └─────────────────────┘       │
│                                                                          │
│   Legend: PK = Primary Key, FK = Foreign Key                            │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Entities

### 1. User (Managed by Better Auth)

Better Auth automatically creates and manages the User entity. We reference it but do not define it.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | VARCHAR(255) | PRIMARY KEY | Unique user identifier (Better Auth generated) |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address |
| name | VARCHAR(255) | NULLABLE | User's display name |
| email_verified | BOOLEAN | DEFAULT FALSE | Email verification status |
| image | TEXT | NULLABLE | Profile image URL |
| created_at | TIMESTAMP | DEFAULT NOW | Account creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW | Last update timestamp |

**Notes:**
- User ID format: Better Auth generates opaque string IDs (e.g., "user_abc123")
- Password is hashed and stored by Better Auth (not exposed in model)
- Additional Better Auth tables (session, account) are auto-managed

---

### 2. Task (Our Entity)

The core entity for todo items, owned by users.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-incrementing task identifier |
| user_id | VARCHAR(255) | FOREIGN KEY, NOT NULL, INDEX | Owner reference to User.id |
| title | VARCHAR(500) | NOT NULL, CHECK(LENGTH > 0) | Task title |
| description | TEXT | NULLABLE, CHECK(LENGTH <= 2000) | Optional task description |
| is_complete | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| created_at | TIMESTAMP WITH TZ | NOT NULL, DEFAULT NOW | Creation timestamp |
| updated_at | TIMESTAMP WITH TZ | NOT NULL, DEFAULT NOW, ON UPDATE | Last modification timestamp |

**Validation Rules:**
- Title: Required, 1-500 characters, non-empty after trimming
- Description: Optional, max 2000 characters
- is_complete: Defaults to false on creation

**Indexes:**
| Index Name | Columns | Purpose |
|------------|---------|---------|
| pk_task | id | Primary key lookup |
| idx_task_user_id | user_id | Filter tasks by user |
| idx_task_user_complete | (user_id, is_complete) | Filter user's complete/pending tasks |
| idx_task_user_created | (user_id, created_at DESC) | Sort user's tasks by date |

**Constraints:**
| Constraint | Rule |
|------------|------|
| task_title_not_empty | LENGTH(TRIM(title)) > 0 |
| task_title_max_length | LENGTH(title) <= 500 |
| task_description_max_length | description IS NULL OR LENGTH(description) <= 2000 |
| fk_task_user | FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE |

---

## SQLModel Definitions

### Task Models (Python)

```python
# backend/app/models/task.py
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func

class TaskBase(SQLModel):
    """Base model with shared task properties."""
    title: str = Field(min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_complete: bool = Field(default=False)

class Task(TaskBase, table=True):
    """Database model for tasks."""
    __tablename__ = "task"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, foreign_key="user.id")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )

class TaskCreate(TaskBase):
    """Schema for creating a task (request body)."""
    pass

class TaskUpdate(TaskBase):
    """Schema for full update (PUT request body)."""
    pass

class TaskPatch(SQLModel):
    """Schema for partial update (PATCH request body)."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_complete: Optional[bool] = None

class TaskRead(TaskBase):
    """Schema for reading a task (response body)."""
    id: int
    created_at: datetime
    updated_at: datetime
```

### TypeScript Types (Frontend)

```typescript
// frontend/lib/types.ts

export interface User {
  id: string;
  email: string;
  name: string | null;
  image: string | null;
}

export interface Task {
  id: number;
  title: string;
  description: string | null;
  is_complete: boolean;
  created_at: string; // ISO 8601 datetime
  updated_at: string; // ISO 8601 datetime
}

export interface TaskCreate {
  title: string;
  description?: string | null;
  is_complete?: boolean;
}

export interface TaskUpdate {
  title: string;
  description: string | null;
  is_complete: boolean;
}

export interface TaskPatch {
  title?: string;
  description?: string | null;
  is_complete?: boolean;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
  limit: number;
  offset: number;
}
```

---

## State Transitions

### Task Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                    TASK STATE TRANSITIONS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────┐     POST /api/tasks      ┌─────────────┐         │
│   │  None   │ ─────────────────────────►│   Pending   │         │
│   └─────────┘                           └─────────────┘         │
│                                               │                  │
│                                               │ PATCH            │
│                                               │ is_complete=true │
│                                               ▼                  │
│                                         ┌─────────────┐         │
│                                         │  Complete   │         │
│                                         └─────────────┘         │
│                                               │                  │
│                                               │ PATCH            │
│                                               │ is_complete=false│
│                                               ▼                  │
│                                         ┌─────────────┐         │
│                                         │   Pending   │◄────────┤
│                                         └─────────────┘         │
│                                               │                  │
│                                               │ DELETE           │
│                                               ▼                  │
│                                         ┌─────────────┐         │
│                                         │   Deleted   │         │
│                                         │ (removed)   │         │
│                                         └─────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**State Rules:**
- Task starts as `Pending` (is_complete=false)
- Can toggle between `Pending` and `Complete`
- Delete is permanent (no soft delete in v1)
- State changes update `updated_at` timestamp

---

## Data Volume Assumptions

| Metric | Assumption | Rationale |
|--------|------------|-----------|
| Users | < 1,000 | Hackathon/demo scale |
| Tasks per user | < 500 | Reasonable personal todo list |
| Total tasks | < 100,000 | Within Neon free tier |
| Request rate | < 100 req/min | Low traffic demo app |

---

## Validation Summary

### Backend Validation (Pydantic/SQLModel)

| Field | Validation | Error Message |
|-------|------------|---------------|
| title | min_length=1 | "ensure this value has at least 1 character" |
| title | max_length=500 | "ensure this value has at most 500 characters" |
| description | max_length=2000 | "ensure this value has at most 2000 characters" |
| is_complete | boolean | "value could not be parsed to a boolean" |

### Frontend Validation (Zod)

```typescript
// frontend/lib/schemas.ts
import { z } from "zod";

export const taskCreateSchema = z.object({
  title: z.string().min(1, "Title is required").max(500, "Title too long"),
  description: z.string().max(2000, "Description too long").optional().nullable(),
  is_complete: z.boolean().optional().default(false),
});

export const taskUpdateSchema = z.object({
  title: z.string().min(1, "Title is required").max(500, "Title too long"),
  description: z.string().max(2000, "Description too long").nullable(),
  is_complete: z.boolean(),
});

export const taskPatchSchema = z.object({
  title: z.string().min(1).max(500).optional(),
  description: z.string().max(2000).optional().nullable(),
  is_complete: z.boolean().optional(),
});
```

---

## References

- specs/database/schema.md - Detailed SQL definitions
- specs/api/rest-endpoints.md - API schema usage
- specs/ui/components.md - Frontend type usage
