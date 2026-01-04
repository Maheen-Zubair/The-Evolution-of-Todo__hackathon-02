# Tasks: CLI Todo App (Phase I)

**Input**: Design documents from `/specs/001-cli-todo-app/`
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/cli-interface.md ✓

**Tests**: Included per plan.md TDD approach ("Implement TDD cycle: write tests first")

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- Exact file paths included in descriptions

## User Story Summary

| Story | Title | Priority | Module Dependencies |
|-------|-------|----------|---------------------|
| US1 | Add New Task | P1 | task.py, task_manager.py, main.py |
| US2 | View All Tasks | P1 | task.py, task_manager.py, main.py |
| US3 | Mark Complete/Incomplete | P2 | task_manager.py, main.py |
| US4 | Update Task Details | P3 | task_manager.py, main.py |
| US5 | Delete Task | P3 | task_manager.py, main.py |

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure: `src/` and `tests/` directories
- [x] T002 [P] Create `src/__init__.py` package marker
- [x] T003 [P] Create `tests/__init__.py` package marker
- [x] T004 [P] Create `pyproject.toml` with pytest dev dependency and project metadata

---

## Phase 2: Foundational (Core Model & Manager)

**Purpose**: Task entity and TaskManager that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Tests for Foundation

- [x] T005 [P] Create unit tests for Task class in `tests/test_task.py`:
  - Test task creation with title and description
  - Test task creation with title only (empty description)
  - Test title validation (empty title rejected)
  - Test title truncation at 500 chars
  - Test description truncation at 2000 chars
  - Test default is_complete=False
  - Test created_at timestamp assignment

- [x] T006 [P] Create unit tests for TaskManager class in `tests/test_task_manager.py`:
  - Test add_task returns Task with auto-increment ID
  - Test get_task by ID returns correct task
  - Test get_task with invalid ID returns None
  - Test get_all_tasks returns list of all tasks
  - Test get_all_tasks returns empty list when no tasks
  - Test update_task modifies title and/or description
  - Test delete_task removes task from storage
  - Test toggle_complete changes is_complete state
  - Test ID counter never decrements after deletion

### Implementation for Foundation

- [x] T007 Implement Task dataclass in `src/task.py`:
  - Fields: id (int), title (str), description (str), is_complete (bool), created_at (datetime)
  - Title validation: non-empty, max 500 chars with truncation
  - Description validation: max 2000 chars with truncation
  - Default values: description="", is_complete=False, created_at=now

- [x] T008 Implement TaskManager class in `src/task_manager.py`:
  - Storage: `tasks: dict[int, Task] = {}`
  - Counter: `next_id: int = 1`
  - Methods: add_task, get_task, get_all_tasks, update_task, delete_task, toggle_complete
  - TaskNotFoundError custom exception

- [x] T009 Run foundation tests and verify all pass: `pytest tests/test_task.py tests/test_task_manager.py -v`

**Checkpoint**: Foundation ready - Task and TaskManager are fully functional and tested

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks with title and optional description via CLI menu

**Independent Test**: Run app → Select "1. Add Task" → Enter title → Verify confirmation message

### Tests for User Story 1

- [x] T010 [P] [US1] Create CLI test for add task flow in `tests/test_main.py`:
  - Test add task with title and description shows success message
  - Test add task with title only shows success message
  - Test add task with empty title shows error and reprompts
  - Test task ID is displayed in confirmation

### Implementation for User Story 1

- [x] T011 [US1] Implement main menu display function in `src/main.py`:
  - Display menu header with borders per cli-interface.md
  - Show 6 numbered options
  - Prompt for user choice (1-6)
  - Validate menu input (reject non-numeric, out of range)

- [x] T012 [US1] Implement add_task_flow() in `src/main.py`:
  - Prompt for title (validate non-empty, reprompt on error)
  - Prompt for description (allow empty with Enter)
  - Call TaskManager.add_task()
  - Display success message: `✓ Task #N created: "title"`

- [x] T013 [US1] Implement main loop in `src/main.py`:
  - Initialize TaskManager instance
  - Display menu, get choice, dispatch to flow functions
  - Return to menu after each operation (except Exit)

- [x] T014 [US1] Run US1 tests and verify all pass: `pytest tests/test_main.py -k "add" -v`

**Checkpoint**: User Story 1 complete - Can add tasks via CLI menu

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can view all tasks with ID, status, title, and description

**Independent Test**: Run app → Add 2-3 tasks → Select "2. View All Tasks" → Verify table display

### Tests for User Story 2

- [x] T015 [P] [US2] Create CLI test for view tasks flow in `tests/test_main.py`:
  - Test view with no tasks shows "No tasks found" message
  - Test view with tasks shows formatted table
  - Test status indicators: [ ] for pending, [x] for complete
  - Test description truncation with "..." for long text
  - Test total count summary at bottom

### Implementation for User Story 2

- [x] T016 [US2] Implement view_tasks_flow() in `src/main.py`:
  - Call TaskManager.get_all_tasks()
  - If empty: display "No tasks found. Add your first task!"
  - If tasks exist: display formatted table per cli-interface.md
  - Truncate description to ~25 chars with "..." if longer
  - Show total count: "Total: N tasks (X complete, Y pending)"

- [x] T017 [US2] Wire view_tasks_flow() to menu option 2 in main loop

- [x] T018 [US2] Run US2 tests and verify all pass: `pytest tests/test_main.py -k "view" -v`

**Checkpoint**: User Stories 1 & 2 complete - MVP functional (add + view)

---

## Phase 5: User Story 3 - Mark Complete/Incomplete (Priority: P2)

**Goal**: Users can toggle task completion status by ID

**Independent Test**: Run app → Add task → Mark complete → View → Verify [x] status → Mark incomplete → Verify [ ] status

### Tests for User Story 3

- [x] T019 [P] [US3] Create CLI test for toggle status flow in `tests/test_main.py`:
  - Test mark pending task as complete shows success message
  - Test mark complete task as pending shows success message
  - Test invalid ID shows "Task not found" error
  - Test non-numeric ID shows "Invalid ID format" error

### Implementation for User Story 3

- [x] T020 [US3] Implement toggle_status_flow() in `src/main.py`:
  - Prompt for task ID to toggle
  - Validate ID format (numeric, positive)
  - Call TaskManager.toggle_complete()
  - Display success: `✓ Task #N "title" marked as complete/pending.`
  - Display error if task not found

- [x] T021 [US3] Wire toggle_status_flow() to menu option 5 in main loop

- [x] T022 [US3] Run US3 tests and verify all pass: `pytest tests/test_main.py -k "toggle or complete" -v`

**Checkpoint**: User Story 3 complete - Can toggle task status

---

## Phase 6: User Story 4 - Update Task Details (Priority: P3)

**Goal**: Users can modify task title and/or description

**Independent Test**: Run app → Add task → Update title → View → Verify new title appears

### Tests for User Story 4

- [x] T023 [P] [US4] Create CLI test for update task flow in `tests/test_main.py`:
  - Test update title only (keep description)
  - Test update description only (keep title)
  - Test update both title and description
  - Test skip update with Enter (keep current values)
  - Test invalid ID shows "Task not found" error

### Implementation for User Story 4

- [x] T024 [US4] Implement update_task_flow() in `src/main.py`:
  - Prompt for task ID to update
  - Validate ID and fetch existing task
  - Show current title, prompt for new (Enter to keep)
  - Show current description, prompt for new (Enter to keep)
  - Call TaskManager.update_task()
  - Display success: `✓ Task #N updated successfully.`

- [x] T025 [US4] Wire update_task_flow() to menu option 3 in main loop

- [x] T026 [US4] Run US4 tests and verify all pass: `pytest tests/test_main.py -k "update" -v`

**Checkpoint**: User Story 4 complete - Can update task details

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Goal**: Users can delete tasks by ID with confirmation

**Independent Test**: Run app → Add task → Delete task → View → Verify task no longer appears

### Tests for User Story 5

- [x] T027 [P] [US5] Create CLI test for delete task flow in `tests/test_main.py`:
  - Test delete with confirmation (y) removes task
  - Test delete with rejection (n) keeps task
  - Test invalid ID shows "Task not found" error
  - Test confirmation prompt shows task title

### Implementation for User Story 5

- [x] T028 [US5] Implement delete_task_flow() in `src/main.py`:
  - Prompt for task ID to delete
  - Validate ID and fetch existing task
  - Show confirmation: `Are you sure you want to delete task #N "title"? (y/n):`
  - If 'y': Call TaskManager.delete_task(), show `✓ Task #N deleted.`
  - If 'n': Show `Deletion cancelled.`

- [x] T029 [US5] Wire delete_task_flow() to menu option 4 in main loop

- [x] T030 [US5] Run US5 tests and verify all pass: `pytest tests/test_main.py -k "delete" -v`

**Checkpoint**: User Story 5 complete - Can delete tasks with confirmation

---

## Phase 8: Exit & Polish

**Purpose**: Exit functionality and cross-cutting concerns

- [x] T031 Implement exit_flow() in `src/main.py`:
  - Display message: `Goodbye! Your tasks were not saved (in-memory only).`
  - Exit the application cleanly

- [x] T032 Wire exit_flow() to menu option 6 in main loop

- [x] T033 [P] Add error handling for unexpected exceptions in main loop

- [x] T034 [P] Add type hints to all functions in `src/task.py`

- [x] T035 [P] Add type hints to all functions in `src/task_manager.py`

- [x] T036 [P] Add type hints to all functions in `src/main.py`

- [x] T037 [P] Add docstrings to all public functions

- [x] T038 Run full test suite: `pytest tests/ -v`

- [x] T039 Run quickstart.md validation: manually test all demo steps

- [x] T040 Verify all success criteria from spec.md are met

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundation) ← BLOCKS ALL USER STORIES
    ↓
┌───┴───┐
↓       ↓
Phase 3 (US1: Add) ──→ Phase 4 (US2: View)  [P1 stories - MVP]
         ↓
    Phase 5 (US3: Toggle)  [P2]
         ↓
    ┌────┴────┐
    ↓         ↓
Phase 6    Phase 7  [P3 stories - can be parallel]
(US4: Update) (US5: Delete)
    └────┬────┘
         ↓
    Phase 8 (Polish)
```

### User Story Dependencies

| Story | Depends On | Can Parallelize With |
|-------|------------|----------------------|
| US1 (Add) | Foundation | - |
| US2 (View) | US1 (need tasks to view) | - |
| US3 (Toggle) | US1 (need tasks to toggle) | - |
| US4 (Update) | US1 (need tasks to update) | US5 |
| US5 (Delete) | US1 (need tasks to delete) | US4 |

### Within Each Phase

1. Tests FIRST (write and verify they FAIL)
2. Implementation SECOND
3. Verify tests PASS
4. Move to next phase

### Parallel Opportunities

**Phase 1 (Setup)**:
```bash
# All can run in parallel:
T002: src/__init__.py
T003: tests/__init__.py
T004: pyproject.toml
```

**Phase 2 (Foundation)**:
```bash
# Tests can run in parallel:
T005: tests/test_task.py
T006: tests/test_task_manager.py
```

**Phase 8 (Polish)**:
```bash
# Type hints can run in parallel:
T034: src/task.py
T035: src/task_manager.py
T036: src/main.py
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundation (CRITICAL)
3. Complete Phase 3: User Story 1 (Add Task)
4. Complete Phase 4: User Story 2 (View Tasks)
5. **STOP and VALIDATE**: Test Add + View flow end-to-end
6. MVP Ready for demo!

### Incremental Delivery

| Increment | Stories | Value Delivered |
|-----------|---------|-----------------|
| MVP | US1 + US2 | Can add and view tasks |
| +Toggle | US3 | Can track completion |
| +Update | US4 | Can correct mistakes |
| +Delete | US5 | Can remove tasks |
| Polish | - | Production ready |

### Single Developer Flow

Execute phases sequentially:
1. Setup → Foundation → US1 → US2 → (MVP!)
2. Continue: US3 → US4 → US5 → Polish

---

## Summary

| Metric | Value |
|--------|-------|
| Total Tasks | 40 |
| Setup Tasks | 4 |
| Foundation Tasks | 5 |
| US1 Tasks | 5 |
| US2 Tasks | 4 |
| US3 Tasks | 4 |
| US4 Tasks | 4 |
| US5 Tasks | 4 |
| Polish Tasks | 10 |
| Parallel Opportunities | 15 tasks marked [P] |
| MVP Scope | Phases 1-4 (US1 + US2) |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Each user story is independently testable after completion
- Commit after each task or logical group
- Run `pytest` after each phase to verify progress
- TDD: Write tests first, verify they fail, then implement
