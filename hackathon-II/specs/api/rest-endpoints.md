---
title: REST API Endpoints for Authenticated Todo Operations
description: Complete REST API specification for multi-user todo CRUD operations with JWT authentication.
version: "1.0"
status: draft
phase: 2
feature: rest-api
created: 2025-12-29
updated: 2025-12-29
authors:
  - Evolution of Todo Team
tags:
  - rest
  - api
  - fastapi
  - crud
  - authentication
dependencies:
  - fastapi
  - sqlmodel
  - pyjwt
related:
  - specs/features/authentication.md
  - specs/database/schema.md
---

# REST API Endpoints for Authenticated Todo Operations

## Overview

Complete REST API specification for multi-user todo CRUD operations with JWT authentication.

**Target Audience**: Backend developers implementing the FastAPI REST API

**Focus**: RESTful design, request/response schemas, error handling, user isolation

## Success Criteria

| ID | Criterion | Measurable Outcome |
|----|-----------|-------------------|
| SC-001 | GET /api/tasks returns user's tasks | Response contains only authenticated user's tasks |
| SC-002 | POST /api/tasks creates task | Returns 201 with created task including generated ID |
| SC-003 | PUT /api/tasks/{id} updates task | Returns 200 with updated task data |
| SC-004 | DELETE /api/tasks/{id} removes task | Returns 204 No Content |
| SC-005 | Invalid task ID returns 404 | Response contains "Task not found" message |
| SC-006 | Cross-user access returns 403 | User cannot access another user's tasks |
| SC-007 | Missing auth returns 401 | All protected endpoints require valid JWT |

## Constraints

| Constraint | Requirement |
|------------|-------------|
| Framework | FastAPI with async/await |
| ORM | SQLModel for Neon PostgreSQL |
| Auth | JWT Bearer token in Authorization header |
| Response Format | JSON with consistent structure |
| Pagination | Default limit 50, max 100 |

## Out of Scope

- GraphQL API
- WebSocket real-time updates
- Batch operations (bulk create/delete)
- Task sharing between users
- File attachments

---

## Clarifications

### Session 2025-01-06

- Q: What does "user isolation" mean in terms of implementation layers? → A: Defense in depth - all database queries filter by user_id AND API middleware validates ownership before any operation

---

## API Base URL

```
Production: https://api.todoapp.com/api
Development: http://localhost:8000/api
```

---

## Authentication

All task endpoints require JWT authentication via Bearer token:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### Authentication Errors

| Status | Condition | Response |
|--------|-----------|----------|
| 401 | Missing Authorization header | `{"detail": "Not authenticated"}` |
| 401 | Invalid/expired token | `{"detail": "Invalid or expired token"}` |
| 403 | User doesn't own resource | `{"detail": "Access denied"}` |

---

## Endpoints

### GET /api/tasks

List all tasks for the authenticated user.

**Request**:
```http
GET /api/tasks?status=all&limit=50&offset=0
Authorization: Bearer {token}
```

**Query Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| status | string | `all` | Filter: `all`, `complete`, `pending` |
| limit | integer | 50 | Max results (1-100) |
| offset | integer | 0 | Pagination offset |
| sort | string | `created_at` | Sort field: `created_at`, `title` |
| order | string | `desc` | Sort order: `asc`, `desc` |

**Success Response** (200 OK):
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Complete project",
      "description": "Finish the todo app implementation",
      "is_complete": false,
      "created_at": "2025-12-29T10:30:00Z",
      "updated_at": "2025-12-29T10:30:00Z"
    },
    {
      "id": 2,
      "title": "Write tests",
      "description": null,
      "is_complete": true,
      "created_at": "2025-12-29T09:00:00Z",
      "updated_at": "2025-12-29T11:00:00Z"
    }
  ],
  "total": 2,
  "limit": 50,
  "offset": 0
}
```

---

### GET /api/tasks/{task_id}

Get a single task by ID.

**Request**:
```http
GET /api/tasks/1
Authorization: Bearer {token}
```

**Path Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| task_id | integer | Task ID |

**Success Response** (200 OK):
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the todo app implementation",
  "is_complete": false,
  "created_at": "2025-12-29T10:30:00Z",
  "updated_at": "2025-12-29T10:30:00Z"
}
```

**Error Response** (404 Not Found):
```json
{
  "detail": "Task 1 not found"
}
```

**Error Response** (403 Forbidden):
```json
{
  "detail": "Access denied"
}
```

---

### POST /api/tasks

Create a new task.

**Request**:
```http
POST /api/tasks
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "New task",
  "description": "Optional description",
  "is_complete": false
}
```

**Request Body**:

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| title | string | Yes | 1-500 characters |
| description | string | No | Max 2000 characters |
| is_complete | boolean | No | Default: false |

**Success Response** (201 Created):
```json
{
  "id": 3,
  "title": "New task",
  "description": "Optional description",
  "is_complete": false,
  "created_at": "2025-12-29T12:00:00Z",
  "updated_at": "2025-12-29T12:00:00Z"
}
```

**Error Response** (422 Unprocessable Entity):
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

### PUT /api/tasks/{task_id}

Fully update an existing task (all fields required).

**Request**:
```http
PUT /api/tasks/1
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description",
  "is_complete": true
}
```

**Request Body**:

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| title | string | Yes | 1-500 characters |
| description | string | Yes | Max 2000 characters (or null) |
| is_complete | boolean | Yes | - |

**Success Response** (200 OK):
```json
{
  "id": 1,
  "title": "Updated title",
  "description": "Updated description",
  "is_complete": true,
  "created_at": "2025-12-29T10:30:00Z",
  "updated_at": "2025-12-29T12:30:00Z"
}
```

---

### PATCH /api/tasks/{task_id}

Partially update an existing task (only provided fields).

**Request**:
```http
PATCH /api/tasks/1
Authorization: Bearer {token}
Content-Type: application/json

{
  "is_complete": true
}
```

**Request Body** (all fields optional):

| Field | Type | Constraints |
|-------|------|-------------|
| title | string | 1-500 characters |
| description | string | Max 2000 characters |
| is_complete | boolean | - |

**Success Response** (200 OK):
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the todo app implementation",
  "is_complete": true,
  "created_at": "2025-12-29T10:30:00Z",
  "updated_at": "2025-12-29T12:45:00Z"
}
```

---

### DELETE /api/tasks/{task_id}

Delete a task.

**Request**:
```http
DELETE /api/tasks/1
Authorization: Bearer {token}
```

**Success Response** (204 No Content):
```
(empty body)
```

**Error Response** (404 Not Found):
```json
{
  "detail": "Task 1 not found"
}
```

---

## Data Models

### TaskCreate (Request)

```python
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_complete: bool = Field(default=False)
```

### TaskUpdate (Request - PUT)

```python
class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    description: Optional[str] = Field(max_length=2000)
    is_complete: bool
```

### TaskPatch (Request - PATCH)

```python
class TaskPatch(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_complete: Optional[bool] = None
```

### TaskRead (Response)

```python
class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_complete: bool
    created_at: datetime
    updated_at: datetime
```

### TaskListResponse (Response)

```python
class TaskListResponse(BaseModel):
    tasks: List[TaskRead]
    total: int
    limit: int
    offset: int
```

---

## Error Handling

### Standard Error Response

```python
class ErrorResponse(BaseModel):
    detail: str
```

### Validation Error Response

```python
class ValidationError(BaseModel):
    detail: List[Dict[str, Any]]
```

### HTTP Status Codes

| Status | Meaning | When Used |
|--------|---------|-----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Malformed request |
| 401 | Unauthorized | Missing/invalid auth |
| 403 | Forbidden | Access denied |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation failed |
| 500 | Internal Server Error | Server error |

---

## Rate Limiting

| Limit Type | Value | Window |
|------------|-------|--------|
| Per User | 100 requests | 1 minute |
| Per IP (unauthenticated) | 20 requests | 1 minute |

**Rate Limit Headers**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1703836860
```

**Rate Limit Exceeded** (429 Too Many Requests):
```json
{
  "detail": "Rate limit exceeded. Try again in 60 seconds."
}
```

---

## Testing Requirements

### Unit Tests

- [ ] TaskCreate validation accepts valid data
- [ ] TaskCreate rejects empty title
- [ ] TaskCreate rejects title > 500 chars
- [ ] TaskPatch allows partial updates
- [ ] Response models serialize correctly

### Integration Tests

- [ ] GET /api/tasks returns only user's tasks
- [ ] POST /api/tasks creates task with correct user_id
- [ ] PUT /api/tasks/{id} updates all fields
- [ ] PATCH /api/tasks/{id} updates only provided fields
- [ ] DELETE /api/tasks/{id} removes task
- [ ] 404 returned for non-existent task
- [ ] 403 returned when accessing another user's task
- [ ] 401 returned without auth header

### Security Tests

- [ ] SQL injection in query params blocked
- [ ] XSS payloads in title/description sanitized
- [ ] CORS headers properly configured
- [ ] Rate limiting enforced

---

## Implementation Checklist

- [ ] Create FastAPI router for /api/tasks
- [ ] Implement TaskCreate, TaskUpdate, TaskPatch schemas
- [ ] Implement TaskRead, TaskListResponse schemas
- [ ] Add JWT authentication dependency
- [ ] Implement GET /api/tasks with filtering
- [ ] Implement GET /api/tasks/{id}
- [ ] Implement POST /api/tasks
- [ ] Implement PUT /api/tasks/{id}
- [ ] Implement PATCH /api/tasks/{id}
- [ ] Implement DELETE /api/tasks/{id}
- [ ] Add user ownership validation
- [ ] Configure rate limiting
- [ ] Write comprehensive tests
- [ ] Generate OpenAPI documentation
