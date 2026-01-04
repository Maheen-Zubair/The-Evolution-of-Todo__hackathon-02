"""TaskManager for CLI Todo App.

This module provides the TaskManager class that handles all CRUD operations
on tasks, maintaining an in-memory dictionary storage as per the data-model.md
specification.
"""

from typing import Optional
from src.task import Task, create_task


class TaskNotFoundError(Exception):
    """Raised when a task with the specified ID is not found."""

    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task #{task_id} not found.")


class TaskManager:
    """Manages task storage and CRUD operations.

    Attributes:
        tasks: Dictionary mapping task IDs to Task objects
        next_id: Counter for auto-incrementing task IDs (never decrements)
    """

    def __init__(self) -> None:
        """Initialize an empty TaskManager."""
        self.tasks: dict[int, Task] = {}
        self.next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task to storage.

        Args:
            title: The task title (required)
            description: Optional task description

        Returns:
            The newly created Task with assigned ID

        Raises:
            ValueError: If title is empty
        """
        task = create_task(self.next_id, title, description)
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task if found, None otherwise
        """
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks as a list.

        Returns:
            List of all tasks in insertion order
        """
        return list(self.tasks.values())

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Task:
        """Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update
            title: New title (if provided)
            description: New description (if provided)

        Returns:
            The updated Task

        Raises:
            TaskNotFoundError: If task with given ID doesn't exist
            ValueError: If new title is empty
        """
        task = self.tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        # Update fields if provided
        if title is not None:
            if not title or not title.strip():
                raise ValueError("Title cannot be empty")
            task.title = title[:500]  # Truncate if needed

        if description is not None:
            task.description = description[:2000]  # Truncate if needed

        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Raises:
            TaskNotFoundError: If task with given ID doesn't exist
        """
        if task_id not in self.tasks:
            raise TaskNotFoundError(task_id)

        del self.tasks[task_id]

    def toggle_complete(self, task_id: int) -> Task:
        """Toggle a task's completion status.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            The updated Task

        Raises:
            TaskNotFoundError: If task with given ID doesn't exist
        """
        task = self.tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        task.is_complete = not task.is_complete
        return task
