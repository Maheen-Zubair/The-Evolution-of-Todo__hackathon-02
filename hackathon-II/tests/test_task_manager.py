"""Unit tests for TaskManager class."""

import pytest
from src.task_manager import TaskManager, TaskNotFoundError


class TestAddTask:
    """Tests for add_task functionality."""

    def test_add_task_returns_task_with_auto_increment_id(self):
        """Test that add_task returns a Task with auto-incremented ID."""
        manager = TaskManager()

        task1 = manager.add_task("First task")
        task2 = manager.add_task("Second task")

        assert task1.id == 1
        assert task2.id == 2

    def test_add_task_with_description(self):
        """Test adding task with description."""
        manager = TaskManager()

        task = manager.add_task("Buy groceries", "Milk, eggs, bread")

        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"


class TestGetTask:
    """Tests for get_task functionality."""

    def test_get_task_by_id_returns_correct_task(self):
        """Test that get_task returns the correct task by ID."""
        manager = TaskManager()
        manager.add_task("Task 1")
        manager.add_task("Task 2")

        task = manager.get_task(1)

        assert task is not None
        assert task.id == 1
        assert task.title == "Task 1"

    def test_get_task_with_invalid_id_returns_none(self):
        """Test that get_task returns None for non-existent ID."""
        manager = TaskManager()
        manager.add_task("Task 1")

        task = manager.get_task(99)

        assert task is None


class TestGetAllTasks:
    """Tests for get_all_tasks functionality."""

    def test_get_all_tasks_returns_list_of_all_tasks(self):
        """Test that get_all_tasks returns all tasks."""
        manager = TaskManager()
        manager.add_task("Task 1")
        manager.add_task("Task 2")
        manager.add_task("Task 3")

        tasks = manager.get_all_tasks()

        assert len(tasks) == 3
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"
        assert tasks[2].title == "Task 3"

    def test_get_all_tasks_returns_empty_list_when_no_tasks(self):
        """Test that get_all_tasks returns empty list when no tasks exist."""
        manager = TaskManager()

        tasks = manager.get_all_tasks()

        assert tasks == []


class TestUpdateTask:
    """Tests for update_task functionality."""

    def test_update_task_modifies_title(self):
        """Test updating task title."""
        manager = TaskManager()
        manager.add_task("Original title", "Original description")

        manager.update_task(1, title="Updated title")
        task = manager.get_task(1)

        assert task.title == "Updated title"
        assert task.description == "Original description"

    def test_update_task_modifies_description(self):
        """Test updating task description."""
        manager = TaskManager()
        manager.add_task("Original title", "Original description")

        manager.update_task(1, description="Updated description")
        task = manager.get_task(1)

        assert task.title == "Original title"
        assert task.description == "Updated description"

    def test_update_task_modifies_both(self):
        """Test updating both title and description."""
        manager = TaskManager()
        manager.add_task("Original title", "Original description")

        manager.update_task(1, title="New title", description="New description")
        task = manager.get_task(1)

        assert task.title == "New title"
        assert task.description == "New description"

    def test_update_nonexistent_task_raises_error(self):
        """Test that updating non-existent task raises TaskNotFoundError."""
        manager = TaskManager()

        with pytest.raises(TaskNotFoundError):
            manager.update_task(99, title="New title")


class TestDeleteTask:
    """Tests for delete_task functionality."""

    def test_delete_task_removes_task_from_storage(self):
        """Test that delete_task removes the task."""
        manager = TaskManager()
        manager.add_task("Task 1")
        manager.add_task("Task 2")

        manager.delete_task(1)

        assert manager.get_task(1) is None
        assert manager.get_task(2) is not None
        assert len(manager.get_all_tasks()) == 1

    def test_delete_nonexistent_task_raises_error(self):
        """Test that deleting non-existent task raises TaskNotFoundError."""
        manager = TaskManager()

        with pytest.raises(TaskNotFoundError):
            manager.delete_task(99)


class TestToggleComplete:
    """Tests for toggle_complete functionality."""

    def test_toggle_complete_changes_is_complete_state(self):
        """Test that toggle_complete flips the is_complete state."""
        manager = TaskManager()
        manager.add_task("Task 1")

        # Initially False
        task = manager.get_task(1)
        assert task.is_complete is False

        # Toggle to True
        manager.toggle_complete(1)
        task = manager.get_task(1)
        assert task.is_complete is True

        # Toggle back to False
        manager.toggle_complete(1)
        task = manager.get_task(1)
        assert task.is_complete is False

    def test_toggle_nonexistent_task_raises_error(self):
        """Test that toggling non-existent task raises TaskNotFoundError."""
        manager = TaskManager()

        with pytest.raises(TaskNotFoundError):
            manager.toggle_complete(99)


class TestIdCounter:
    """Tests for ID counter behavior."""

    def test_id_counter_never_decrements_after_deletion(self):
        """Test that ID counter continues incrementing after deletion."""
        manager = TaskManager()

        task1 = manager.add_task("Task 1")  # ID 1
        task2 = manager.add_task("Task 2")  # ID 2

        manager.delete_task(1)

        task3 = manager.add_task("Task 3")  # Should be ID 3, not ID 1

        assert task3.id == 3
