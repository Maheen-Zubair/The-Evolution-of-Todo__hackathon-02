"""Integration tests for CLI Todo App main module."""

import pytest
from io import StringIO
from unittest.mock import patch
from src.main import (
    display_menu,
    add_task_flow,
    view_tasks_flow,
    toggle_status_flow,
    update_task_flow,
    delete_task_flow,
)
from src.task_manager import TaskManager


class TestAddTaskFlow:
    """Tests for add task CLI flow (US1)."""

    def test_add_task_with_title_and_description_shows_success(self):
        """Test adding task with title and description shows success message."""
        manager = TaskManager()

        with patch("builtins.input", side_effect=["Buy groceries", "Milk, eggs"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                add_task_flow(manager)
                output = mock_stdout.getvalue()

        assert '✓ Task #1 created: "Buy groceries"' in output

    def test_add_task_with_title_only_shows_success(self):
        """Test adding task with title only shows success message."""
        manager = TaskManager()

        with patch("builtins.input", side_effect=["Call mom", ""]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                add_task_flow(manager)
                output = mock_stdout.getvalue()

        assert '✓ Task #1 created: "Call mom"' in output

    def test_add_task_empty_title_shows_error_and_reprompts(self):
        """Test that empty title shows error and reprompts."""
        manager = TaskManager()

        # First empty, then valid title
        with patch("builtins.input", side_effect=["", "Valid title", "desc"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                add_task_flow(manager)
                output = mock_stdout.getvalue()

        assert "Error: Title cannot be empty" in output
        assert '✓ Task #1 created: "Valid title"' in output

    def test_task_id_displayed_in_confirmation(self):
        """Test that task ID is displayed in confirmation message."""
        manager = TaskManager()

        # Add first task
        with patch("builtins.input", side_effect=["Task 1", ""]):
            with patch("sys.stdout", new_callable=StringIO):
                add_task_flow(manager)

        # Add second task
        with patch("builtins.input", side_effect=["Task 2", ""]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                add_task_flow(manager)
                output = mock_stdout.getvalue()

        assert "Task #2" in output


class TestViewTasksFlow:
    """Tests for view tasks CLI flow (US2)."""

    def test_view_no_tasks_shows_message(self):
        """Test viewing empty task list shows appropriate message."""
        manager = TaskManager()

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            view_tasks_flow(manager)
            output = mock_stdout.getvalue()

        assert "No tasks found. Add your first task!" in output

    def test_view_tasks_shows_formatted_table(self):
        """Test viewing tasks shows formatted table."""
        manager = TaskManager()
        manager.add_task("Buy groceries", "Milk, eggs")
        manager.add_task("Call mom", "")

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            view_tasks_flow(manager)
            output = mock_stdout.getvalue()

        assert "ID" in output
        assert "Status" in output
        assert "Title" in output
        assert "Buy groceries" in output
        assert "Call mom" in output

    def test_view_tasks_status_indicators(self):
        """Test that status indicators show correctly."""
        manager = TaskManager()
        manager.add_task("Pending task")
        manager.add_task("Complete task")
        manager.toggle_complete(2)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            view_tasks_flow(manager)
            output = mock_stdout.getvalue()

        assert "[ ]" in output  # Pending
        assert "[x]" in output  # Complete

    def test_view_tasks_description_truncation(self):
        """Test that long descriptions are truncated with ellipsis."""
        manager = TaskManager()
        long_desc = "A" * 100
        manager.add_task("Long desc task", long_desc)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            view_tasks_flow(manager)
            output = mock_stdout.getvalue()

        assert "..." in output

    def test_view_tasks_total_count_summary(self):
        """Test that total count summary is shown."""
        manager = TaskManager()
        manager.add_task("Task 1")
        manager.add_task("Task 2")
        manager.add_task("Task 3")
        manager.toggle_complete(1)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            view_tasks_flow(manager)
            output = mock_stdout.getvalue()

        assert "Total: 3 tasks" in output
        assert "1 complete" in output
        assert "2 pending" in output


class TestToggleStatusFlow:
    """Tests for toggle status CLI flow (US3)."""

    def test_mark_pending_task_complete_shows_success(self):
        """Test marking pending task as complete shows success."""
        manager = TaskManager()
        manager.add_task("Task 1")

        with patch("builtins.input", return_value="1"):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                toggle_status_flow(manager)
                output = mock_stdout.getvalue()

        assert 'Task #1 "Task 1" marked as complete' in output

    def test_mark_complete_task_pending_shows_success(self):
        """Test marking complete task as pending shows success."""
        manager = TaskManager()
        manager.add_task("Task 1")
        manager.toggle_complete(1)  # Now complete

        with patch("builtins.input", return_value="1"):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                toggle_status_flow(manager)
                output = mock_stdout.getvalue()

        assert 'Task #1 "Task 1" marked as pending' in output

    def test_invalid_id_shows_task_not_found(self):
        """Test that invalid ID shows task not found error."""
        manager = TaskManager()

        with patch("builtins.input", return_value="99"):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                toggle_status_flow(manager)
                output = mock_stdout.getvalue()

        assert "Error: Task #99 not found" in output

    def test_non_numeric_id_shows_invalid_format(self):
        """Test that non-numeric ID shows invalid format error."""
        manager = TaskManager()

        with patch("builtins.input", return_value="abc"):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                toggle_status_flow(manager)
                output = mock_stdout.getvalue()

        assert "Error: Invalid ID format" in output


class TestUpdateTaskFlow:
    """Tests for update task CLI flow (US4)."""

    def test_update_title_only(self):
        """Test updating only the title."""
        manager = TaskManager()
        manager.add_task("Original title", "Original desc")

        with patch("builtins.input", side_effect=["1", "New title", ""]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                update_task_flow(manager)
                output = mock_stdout.getvalue()

        assert "Task #1 updated successfully" in output
        assert manager.get_task(1).title == "New title"
        assert manager.get_task(1).description == "Original desc"

    def test_update_description_only(self):
        """Test updating only the description."""
        manager = TaskManager()
        manager.add_task("Original title", "Original desc")

        with patch("builtins.input", side_effect=["1", "", "New desc"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                update_task_flow(manager)
                output = mock_stdout.getvalue()

        assert "Task #1 updated successfully" in output
        assert manager.get_task(1).title == "Original title"
        assert manager.get_task(1).description == "New desc"

    def test_update_both_title_and_description(self):
        """Test updating both title and description."""
        manager = TaskManager()
        manager.add_task("Original title", "Original desc")

        with patch("builtins.input", side_effect=["1", "New title", "New desc"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                update_task_flow(manager)
                output = mock_stdout.getvalue()

        assert "Task #1 updated successfully" in output
        task = manager.get_task(1)
        assert task.title == "New title"
        assert task.description == "New desc"

    def test_skip_update_keeps_current_values(self):
        """Test pressing Enter keeps current values."""
        manager = TaskManager()
        manager.add_task("Original title", "Original desc")

        with patch("builtins.input", side_effect=["1", "", ""]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                update_task_flow(manager)
                output = mock_stdout.getvalue()

        assert "Task #1 updated successfully" in output
        task = manager.get_task(1)
        assert task.title == "Original title"
        assert task.description == "Original desc"

    def test_invalid_id_shows_task_not_found(self):
        """Test that invalid ID shows task not found error."""
        manager = TaskManager()

        with patch("builtins.input", return_value="99"):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                update_task_flow(manager)
                output = mock_stdout.getvalue()

        assert "Error: Task #99 not found" in output


class TestDeleteTaskFlow:
    """Tests for delete task CLI flow (US5)."""

    def test_delete_with_confirmation_removes_task(self):
        """Test deleting task with 'y' confirmation removes it."""
        manager = TaskManager()
        manager.add_task("Task to delete")

        with patch("builtins.input", side_effect=["1", "y"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                delete_task_flow(manager)
                output = mock_stdout.getvalue()

        assert "Task #1 deleted" in output
        assert manager.get_task(1) is None

    def test_delete_with_rejection_keeps_task(self):
        """Test rejecting deletion with 'n' keeps the task."""
        manager = TaskManager()
        manager.add_task("Task to keep")

        with patch("builtins.input", side_effect=["1", "n"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                delete_task_flow(manager)
                output = mock_stdout.getvalue()

        assert "Deletion cancelled" in output
        assert manager.get_task(1) is not None

    def test_invalid_id_shows_task_not_found(self):
        """Test that invalid ID shows task not found error."""
        manager = TaskManager()

        with patch("builtins.input", return_value="99"):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                delete_task_flow(manager)
                output = mock_stdout.getvalue()

        assert "Error: Task #99 not found" in output

    def test_confirmation_prompt_shows_task_title(self):
        """Test confirmation prompt includes task title."""
        manager = TaskManager()
        manager.add_task("Important task")

        # Capture the input call to verify the prompt contains task title
        with patch("builtins.input", side_effect=["1", "n"]) as mock_input:
            with patch("sys.stdout", new_callable=StringIO):
                delete_task_flow(manager)

        # The second input call should be the confirmation prompt with the task title
        calls = mock_input.call_args_list
        assert len(calls) == 2
        confirm_prompt = calls[1][0][0]  # Get the prompt string from second call
        assert "Important task" in confirm_prompt
