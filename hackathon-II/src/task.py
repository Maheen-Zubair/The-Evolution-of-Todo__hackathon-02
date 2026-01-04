"""Task entity definition for CLI Todo App.

This module defines the Task dataclass representing a single todo item
with validation rules per the data-model.md specification.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


# Constants for validation
MAX_TITLE_LENGTH = 500
MAX_DESCRIPTION_LENGTH = 2000


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique integer identifier (auto-assigned, starts from 1)
        title: Short name/summary of the task (required, max 500 chars)
        description: Detailed information about the task (optional, max 2000 chars)
        is_complete: Boolean indicating completion status (default: False)
        created_at: Timestamp when task was created (immutable after creation)
    """

    id: int
    title: str
    description: str = ""
    is_complete: bool = False
    created_at: datetime = field(default_factory=datetime.now)


def create_task(
    task_id: int,
    title: str,
    description: str = "",
) -> Task:
    """Create a new Task with validation.

    Args:
        task_id: The unique ID for this task
        title: The task title (required, non-empty)
        description: Optional task description

    Returns:
        A new Task instance

    Raises:
        ValueError: If title is empty or whitespace-only
    """
    # Validate title
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")

    # Truncate if needed
    validated_title = title[:MAX_TITLE_LENGTH]
    validated_description = description[:MAX_DESCRIPTION_LENGTH]

    return Task(
        id=task_id,
        title=validated_title,
        description=validated_description,
        is_complete=False,
        created_at=datetime.now(),
    )
