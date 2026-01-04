# CLI Interface Contract: CLI Todo App (Phase I)

**Feature**: 001-cli-todo-app
**Date**: 2025-12-29
**Type**: Command-Line Interface (Menu-Driven)

## Interface Overview

The CLI provides a menu-driven interface for all task operations. No REST API is needed for Phase I (in-memory, single-user).

## Main Menu

```
========================================
       TODO APP - Main Menu
========================================

1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit

Enter your choice (1-6):
```

## Operation Contracts

### 1. Add Task

**Input Flow**:
```
Enter task title: <user input>
Enter task description (optional, press Enter to skip): <user input>
```

**Success Output**:
```
✓ Task #1 created: "Buy groceries"
```

**Error Output** (empty title):
```
✗ Error: Title cannot be empty. Please try again.
Enter task title:
```

### 2. View All Tasks

**Success Output** (tasks exist):
```
========================================
            YOUR TASKS
========================================
ID  | Status | Title                     | Description
----|--------|---------------------------|---------------------------
1   | [ ]    | Buy groceries             | Milk, eggs, bread
2   | [x]    | Call mom                  |
3   | [ ]    | Finish report             | Due by Friday, need to...
========================================
Total: 3 tasks (1 complete, 2 pending)
```

**Output** (no tasks):
```
========================================
            YOUR TASKS
========================================
No tasks found. Add your first task!
========================================
```

### 3. Update Task

**Input Flow**:
```
Enter task ID to update: <user input>
Current title: "Buy groceries"
Enter new title (press Enter to keep current): <user input>
Current description: "Milk, eggs, bread"
Enter new description (press Enter to keep current): <user input>
```

**Success Output**:
```
✓ Task #1 updated successfully.
```

**Error Output** (task not found):
```
✗ Error: Task #99 not found.
```

**Error Output** (invalid ID):
```
✗ Error: Invalid ID format. Please enter a number.
```

### 4. Delete Task

**Input Flow**:
```
Enter task ID to delete: <user input>
Are you sure you want to delete task #1 "Buy groceries"? (y/n): <user input>
```

**Success Output**:
```
✓ Task #1 deleted.
```

**Error Output** (task not found):
```
✗ Error: Task #99 not found.
```

**Cancelled Output**:
```
Deletion cancelled.
```

### 5. Mark Complete/Incomplete

**Input Flow**:
```
Enter task ID to toggle status: <user input>
```

**Success Output** (marking complete):
```
✓ Task #1 "Buy groceries" marked as complete.
```

**Success Output** (marking incomplete):
```
✓ Task #1 "Buy groceries" marked as pending.
```

**Error Output** (task not found):
```
✗ Error: Task #99 not found.
```

### 6. Exit

**Output**:
```
Goodbye! Your tasks were not saved (in-memory only).
```

## Error Handling

| Error Condition | Message |
|-----------------|---------|
| Empty title | "Error: Title cannot be empty." |
| Title too long | "Warning: Title truncated to 500 characters." |
| Description too long | "Warning: Description truncated to 2000 characters." |
| Task not found | "Error: Task #[ID] not found." |
| Invalid ID format | "Error: Invalid ID format. Please enter a number." |
| Invalid menu choice | "Error: Invalid choice. Please enter 1-6." |
| Negative/zero ID | "Error: Invalid ID. Task IDs start from 1." |

## Status Indicators

| Status | Display |
|--------|---------|
| Pending | `[ ]` |
| Complete | `[x]` |

## Return to Menu

After each operation (except Exit), the system automatically returns to the main menu.
