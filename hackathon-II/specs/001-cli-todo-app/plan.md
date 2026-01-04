# Implementation Plan: CLI Todo App (Phase I)

**Branch**: `001-cli-todo-app` | **Date**: 2025-12-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-cli-todo-app/spec.md`

## Summary

Build an in-memory CLI todo application using Python 3.13+ with standard library only. The application provides a menu-driven interface for CRUD operations on tasks (Add, View, Update, Delete, Mark Complete/Incomplete). Uses dictionary-based storage for O(1) lookups by task ID. Three-module architecture separates data model, business logic, and user interface.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (standard library only)
**Storage**: In-memory dictionary (`dict[int, Task]`)
**Testing**: pytest (dev dependency only)
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux)
**Project Type**: Single project
**Performance Goals**: <1s startup, <2s for viewing up to 1000 tasks
**Constraints**: No persistence, single-user, in-memory only
**Scale/Scope**: Single user, unlimited tasks per session (memory-limited)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Accuracy | ✅ PASS | Clear requirements, no ambiguity |
| Clarity | ✅ PASS | Menu-driven UI, beginner-friendly |
| Reproducibility | ✅ PASS | No external dependencies, standard library |
| Rigor | ✅ PASS | pytest testing, PEP 8 compliance |
| Security | ✅ PASS | No auth needed (single-user, in-memory) |
| Testing | ✅ PASS | Unit + integration tests planned |
| Documentation | ✅ PASS | Spec, plan, contracts documented |

**Phase I Constraints Met**:
- ✅ Python 3.13+
- ✅ CLI-based interface
- ✅ In-memory storage only
- ✅ Beginner-friendly implementation

## Project Structure

### Documentation (this feature)

```text
specs/001-cli-todo-app/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Technical decisions
├── data-model.md        # Task entity definition
├── quickstart.md        # Setup and run instructions
├── contracts/
│   └── cli-interface.md # CLI menu contracts
├── checklists/
│   └── requirements.md  # Implementation checklist
└── tasks.md             # Created by /sp.tasks (next step)
```

### Source Code (repository root)

```text
src/
├── __init__.py          # Package marker
├── task.py              # Task dataclass with validation
├── task_manager.py      # TaskManager class with CRUD operations
└── main.py              # CLI menu loop and user interaction

tests/
├── __init__.py          # Package marker
├── test_task.py         # Unit tests for Task class
├── test_task_manager.py # Unit tests for TaskManager
└── test_main.py         # Integration tests for CLI
```

**Structure Decision**: Single project structure selected. Web/mobile options not applicable for Phase I CLI application. The three-module design follows MVC-like separation:
- `task.py` = Model (data structure)
- `task_manager.py` = Controller (business logic)
- `main.py` = View (user interface)

## Complexity Tracking

No constitution violations. Implementation is minimal:
- 3 source files only
- No external dependencies
- No database or ORM
- No async/concurrency
- No network operations

## Implementation Phases

### Phase 0: Research (Complete)

See [research.md](./research.md) for technical decisions:
1. Dictionary storage for O(1) lookups ✓
2. Auto-increment integer IDs ✓
3. Boolean `is_complete` status ✓
4. Menu-driven interface ✓
5. Python 3.13+ standard library ✓
6. Three-module architecture ✓

### Phase 1: Design (Complete)

**Artifacts created**:
- [data-model.md](./data-model.md) - Task entity with validation rules
- [contracts/cli-interface.md](./contracts/cli-interface.md) - CLI menu contracts
- [quickstart.md](./quickstart.md) - Setup and run instructions

### Phase 2: Task Generation (Next)

Run `/sp.tasks` to generate implementation tasks from this plan.

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Storage | `dict[int, Task]` | O(1) lookup by ID, insertion order preserved |
| ID Generation | Auto-increment from 1 | User-friendly, predictable |
| Status Tracking | Boolean `is_complete` | Binary state, simple toggle |
| CLI Style | Menu-driven | Beginner-friendly, discoverable |
| Dependencies | None | Minimal setup, constitution compliant |
| Architecture | 3 modules | Separation of concerns, testable |

## Testing Strategy

| Layer | Scope | Tools |
|-------|-------|-------|
| Unit | Task class validation | pytest |
| Unit | TaskManager CRUD operations | pytest |
| Integration | CLI menu flows | pytest + input mocking |

**Test Coverage Goals**:
- All functional requirements (FR-001 to FR-011)
- All edge cases from spec
- Error handling paths

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Input validation gaps | Low | Medium | Comprehensive edge case tests |
| Menu flow bugs | Low | Low | Integration tests with mocked input |
| Performance with many tasks | Very Low | Low | Dictionary provides O(1) ops |

## Success Criteria Verification

| Criteria | Implementation |
|----------|----------------|
| SC-001: Add task <30s | Menu-driven, minimal steps |
| SC-002: View tasks <2s | O(1) dictionary iteration |
| SC-003: ≤3 interactions | Direct menu options |
| SC-004: 100% ops succeed | Input validation, error handling |
| SC-005: Clear errors | Specific error messages per type |
| SC-006: Learn in 5min | Numbered menu, intuitive labels |
| SC-007: Start <1s | No deps, minimal init |

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Implement TDD cycle: write tests first, then code
3. Verify all success criteria after implementation
4. Run full test suite before marking complete
