# Data Model: CLI Todo App (Phase I)

**Feature**: 001-cli-todo-app
**Date**: 2025-12-29
**Source**: spec.md Key Entities section

## Entities

### Task

Represents a single todo item managed by the application.

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| id | int | Yes | Auto-assigned | Unique, starts from 1, auto-increment |
| title | str | Yes | N/A | Non-empty, max 500 characters |
| description | str | No | "" | Max 2000 characters |
| is_complete | bool | Yes | False | True = complete, False = pending |
| created_at | datetime | Yes | Current time | Immutable after creation |

### Validation Rules

1. **Title validation**:
   - MUST NOT be empty or whitespace-only
   - MUST NOT exceed 500 characters
   - Truncated to 500 chars if longer (with warning)

2. **Description validation**:
   - MAY be empty (optional field)
   - MUST NOT exceed 2000 characters
   - Truncated to 2000 chars if longer (with warning)

3. **ID validation**:
   - MUST be positive integer (≥ 1)
   - MUST be unique within session
   - IDs are NOT reused after deletion

### State Transitions

```
                    mark_complete()
    ┌─────────┐  ─────────────────►  ┌───────────┐
    │ PENDING │                       │ COMPLETE  │
    └─────────┘  ◄─────────────────  └───────────┘
                   mark_incomplete()
```

**Valid Transitions**:
- PENDING → COMPLETE (via mark_complete)
- COMPLETE → PENDING (via mark_incomplete)
- Task can be created only in PENDING state
- Task can be deleted from any state

### Task Lifecycle

1. **Creation**: Task created with title (required) and description (optional)
   - ID auto-assigned from counter
   - is_complete set to False
   - created_at set to current timestamp

2. **Read**: Tasks retrieved by ID or as full list
   - Display truncates description to 50 chars with "..."

3. **Update**: Title and/or description can be modified
   - ID and created_at are immutable
   - is_complete modified only via toggle

4. **Delete**: Task removed from storage
   - ID is NOT reused

5. **Status Toggle**: is_complete toggled between True/False

## Storage Model

### In-Memory Dictionary

```python
# Storage structure
tasks: dict[int, Task] = {}

# ID counter (never decrements)
next_id: int = 1
```

**Operations**:
| Operation | Complexity | Implementation |
|-----------|------------|----------------|
| Add | O(1) | `tasks[next_id] = task; next_id += 1` |
| Get by ID | O(1) | `tasks.get(id)` |
| Get all | O(n) | `list(tasks.values())` |
| Update | O(1) | `tasks[id] = updated_task` |
| Delete | O(1) | `del tasks[id]` |

## Display Format

### Task List View
```
ID  | Status | Title                          | Description
----|--------|--------------------------------|---------------------------
1   | [ ]    | Buy groceries                  | Milk, eggs, bread
2   | [x]    | Call mom                       |
3   | [ ]    | Finish report                  | Due by Friday, need to...
```

### Single Task View
```
Task #1
Title: Buy groceries
Description: Milk, eggs, bread
Status: Pending
Created: 2025-12-29 10:30:00
```
