# Quickstart: CLI Todo App (Phase I)

**Feature**: 001-cli-todo-app
**Date**: 2025-12-29

## Prerequisites

- Python 3.13+ installed
- Terminal/command prompt access
- No external dependencies required

## Setup

### 1. Clone and Navigate

```bash
cd hackathon-II
```

### 2. Verify Python Version

```bash
python --version
# Expected: Python 3.13.x or higher
```

### 3. Project Structure

After implementation, the source structure will be:

```
src/
├── __init__.py
├── task.py           # Task class definition
├── task_manager.py   # CRUD operations
└── main.py           # CLI menu interface

tests/
├── __init__.py
├── test_task.py
├── test_task_manager.py
└── test_main.py
```

## Running the Application

### Start the CLI

```bash
python -m src.main
```

Or directly:

```bash
python src/main.py
```

### Expected Output

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

## Quick Demo

### Add Your First Task

1. Select option `1` (Add Task)
2. Enter title: `Buy groceries`
3. Enter description: `Milk, eggs, bread`
4. See confirmation: `✓ Task #1 created: "Buy groceries"`

### View Tasks

1. Select option `2` (View All Tasks)
2. See your task listed with ID, status, title, and description

### Mark Complete

1. Select option `5` (Mark Complete/Incomplete)
2. Enter task ID: `1`
3. See confirmation: `✓ Task #1 "Buy groceries" marked as complete.`

### Exit

1. Select option `6` (Exit)
2. See message: `Goodbye! Your tasks were not saved (in-memory only).`

## Running Tests

### Install pytest (dev dependency)

```bash
pip install pytest
```

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Modules

```bash
# Task model tests
pytest tests/test_task.py -v

# Task manager tests
pytest tests/test_task_manager.py -v

# CLI integration tests
pytest tests/test_main.py -v
```

### Expected Test Output

```
tests/test_task.py::test_task_creation PASSED
tests/test_task.py::test_task_title_validation PASSED
tests/test_task_manager.py::test_add_task PASSED
tests/test_task_manager.py::test_get_all_tasks PASSED
...
```

## Troubleshooting

### Python Not Found

Ensure Python 3.13+ is installed and in your PATH:

```bash
# Windows
py --version

# macOS/Linux
python3 --version
```

### Module Not Found

Run from the project root directory:

```bash
cd hackathon-II
python -m src.main
```

### Permission Denied

Ensure files have execute permissions (Linux/macOS):

```bash
chmod +x src/main.py
```

## Next Steps

After completing Phase I:

1. Run all tests to verify implementation
2. Check success criteria in spec.md
3. Proceed to Phase II (persistent storage) when ready
