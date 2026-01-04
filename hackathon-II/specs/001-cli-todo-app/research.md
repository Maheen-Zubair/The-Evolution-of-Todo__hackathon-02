# Research: CLI Todo App (Phase I)

**Feature**: 001-cli-todo-app
**Date**: 2025-12-29
**Status**: Complete

## Technical Decisions

### 1. Task Storage: Dictionary vs List

**Decision**: Use a dictionary with task ID as key

**Rationale**:
- O(1) lookup by ID for all operations (mark complete, update, delete)
- List would require O(n) search for every operation
- Dictionary maintains insertion order in Python 3.7+
- ID-based access is the primary access pattern in this CLI

**Alternatives Considered**:
- List with linear search: Simpler but O(n) for lookups
- List with index as ID: Problematic when tasks are deleted (IDs shift)
- SQLite: Overkill for in-memory Phase I; reserved for Phase II

### 2. Task ID Generation: Auto-increment vs UUID

**Decision**: Auto-increment integer starting from 1

**Rationale**:
- Simpler for CLI users to type (1, 2, 3 vs UUID strings)
- Predictable ordering by creation time
- Constitution specifies "beginner-friendly" for Phase I
- UUID reserved for future multi-user Phase II

**Alternatives Considered**:
- UUID: Better for distributed systems, but unnecessary complexity for single-user CLI
- Timestamp-based: Less intuitive for users

### 3. Status Tracking: Boolean vs String/Enum

**Decision**: Boolean `is_complete` field

**Rationale**:
- Spec explicitly defines only two states: pending and complete
- Boolean is simplest representation for binary state
- Easily extensible to enum in Phase II if needed
- Clear toggle semantics for mark complete/incomplete

**Alternatives Considered**:
- String ("pending", "complete"): More human-readable but error-prone
- Enum: Type-safe but overkill for two states

### 4. CLI Input Handling: Menu-driven vs Command Parsing

**Decision**: Menu-driven interface with numbered options

**Rationale**:
- Constitution specifies "beginner-friendly" audience
- Clear discoverability of all features
- Reduces user input errors
- Matches success criteria SC-003: "3 or fewer menu interactions"

**Alternatives Considered**:
- Command parsing (e.g., `add "title"`): More scalable but higher learning curve
- Both: Complexity not justified for Phase I

### 5. Python Version and Dependencies

**Decision**: Python 3.13+ with standard library only

**Rationale**:
- User explicitly specified Python 3.13+
- No external dependencies minimizes setup complexity
- datetime module for timestamps (standard library)
- Future pytest for testing (dev dependency only)

**Alternatives Considered**:
- Rich library for UI: Nice-to-have but adds dependency
- Click for CLI: Overkill for menu-driven interface

### 6. Project Structure

**Decision**: Single project with 3 core modules

**Rationale**:
- Follows separation of concerns (MVC-like pattern)
- `task.py`: Data model (Model)
- `task_manager.py`: Business logic (Controller)
- `main.py`: User interface (View)
- Modular design enables easy testing

**Structure**:
```
src/
├── __init__.py
├── task.py           # Task class definition
├── task_manager.py   # CRUD operations
└── main.py          # CLI menu interface

tests/
├── __init__.py
├── test_task.py
├── test_task_manager.py
└── test_main.py
```

## Best Practices Applied

### Python PEP 8 Compliance
- Snake_case for functions and variables
- PascalCase for classes
- Type hints for all function signatures
- Docstrings for all public functions

### Error Handling
- Custom exceptions for domain errors (TaskNotFoundError)
- Input validation at service layer
- User-friendly error messages at CLI layer

### Testing Strategy
- Unit tests for Task class
- Unit tests for TaskManager (mock-free, in-memory)
- Integration tests for CLI flows (using subprocess or input mocking)

## References

- Python 3.13 Documentation: https://docs.python.org/3.13/
- PEP 8 Style Guide: https://peps.python.org/pep-0008/
- Constitution Phase I requirements: `.specify/memory/constitution.md`
