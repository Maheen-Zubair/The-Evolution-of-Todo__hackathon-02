"""Unit tests for Task class."""

import pytest
from datetime import datetime
from src.task import Task, create_task


class TestTaskCreation:
    """Tests for task creation functionality."""

    def test_task_creation_with_title_and_description(self):
        """Test creating a task with both title and description."""
        task = create_task(1, "Buy groceries", "Milk, eggs, bread")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"
        assert task.is_complete is False
        assert isinstance(task.created_at, datetime)

    def test_task_creation_with_title_only(self):
        """Test creating a task with title only (empty description)."""
        task = create_task(1, "Call mom")

        assert task.id == 1
        assert task.title == "Call mom"
        assert task.description == ""
        assert task.is_complete is False

    def test_task_creation_with_empty_description(self):
        """Test creating a task with explicit empty description."""
        task = create_task(1, "Call mom", "")

        assert task.description == ""


class TestTitleValidation:
    """Tests for title validation."""

    def test_empty_title_rejected(self):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            create_task(1, "")

    def test_whitespace_only_title_rejected(self):
        """Test that whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            create_task(1, "   ")

    def test_title_truncation_at_500_chars(self):
        """Test that title is truncated to 500 characters."""
        long_title = "A" * 600
        task = create_task(1, long_title)

        assert len(task.title) == 500
        assert task.title == "A" * 500


class TestDescriptionValidation:
    """Tests for description validation."""

    def test_description_truncation_at_2000_chars(self):
        """Test that description is truncated to 2000 characters."""
        long_description = "B" * 2500
        task = create_task(1, "Test task", long_description)

        assert len(task.description) == 2000
        assert task.description == "B" * 2000


class TestDefaultValues:
    """Tests for default values."""

    def test_default_is_complete_false(self):
        """Test that is_complete defaults to False."""
        task = create_task(1, "Test task")

        assert task.is_complete is False

    def test_created_at_timestamp_assigned(self):
        """Test that created_at is assigned a datetime."""
        before = datetime.now()
        task = create_task(1, "Test task")
        after = datetime.now()

        assert before <= task.created_at <= after
