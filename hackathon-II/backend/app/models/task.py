"""
Phase 2 Full-Stack Todo App - Task Model

SQLModel entity definitions for tasks with validation.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, func, Index
from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    """Base model with shared task properties."""

    title: str = Field(min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_complete: bool = Field(default=False)


class Task(TaskBase, table=True):
    """Database model for tasks."""

    __tablename__ = "task"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        ),
    )

    # Additional indexes for common query patterns
    __table_args__ = (
        Index("idx_task_user_complete", "user_id", "is_complete"),
        Index("idx_task_user_created", "user_id", "created_at"),
    )


class TaskCreate(TaskBase):
    """Schema for creating a task (POST request body)."""

    pass


class TaskUpdate(TaskBase):
    """Schema for full update (PUT request body)."""

    pass


class TaskPatch(SQLModel):
    """Schema for partial update (PATCH request body)."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_complete: Optional[bool] = None


class TaskRead(TaskBase):
    """Schema for reading a task (response body)."""

    id: int
    created_at: datetime
    updated_at: datetime


class TaskListResponse(SQLModel):
    """Schema for list tasks response with pagination."""

    tasks: list[TaskRead]
    total: int
    limit: int
    offset: int
