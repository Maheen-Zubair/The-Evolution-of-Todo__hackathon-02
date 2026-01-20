"""
Phase 2 Full-Stack Todo App - Tasks Router

REST API endpoints for task CRUD operations with user isolation.
"""

from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, func, select

from app.db import get_session
from app.dependencies import AuthenticatedUser
from app.models import (
    Task,
    TaskCreate,
    TaskListResponse,
    TaskPatch,
    TaskRead,
    TaskUpdate,
)

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=TaskListResponse)
def list_tasks(
    current_user: AuthenticatedUser,
    session: Session = Depends(get_session),
    status_filter: Optional[Literal["all", "complete", "pending"]] = Query(
        default="all", alias="status"
    ),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    sort: Literal["created_at", "title"] = Query(default="created_at"),
    order: Literal["asc", "desc"] = Query(default="desc"),
) -> TaskListResponse:
    """
    List all tasks for the authenticated user.

    - **status**: Filter by completion status (all, complete, pending)
    - **limit**: Maximum number of results (1-100, default 50)
    - **offset**: Pagination offset (default 0)
    - **sort**: Sort field (created_at, title)
    - **order**: Sort order (asc, desc)
    """
    # Base query with user isolation (defense in depth)
    query = select(Task).where(Task.user_id == current_user.id)

    # Apply status filter
    if status_filter == "complete":
        query = query.where(Task.is_complete == True)  # noqa: E712
    elif status_filter == "pending":
        query = query.where(Task.is_complete == False)  # noqa: E712

    # Count total before pagination
    count_query = select(func.count()).select_from(
        query.subquery()
    )
    total = session.exec(count_query).one()

    # Apply sorting
    sort_column = getattr(Task, sort)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Apply pagination
    query = query.offset(offset).limit(limit)

    tasks = session.exec(query).all()

    return TaskListResponse(
        tasks=[TaskRead.model_validate(task) for task in tasks],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    current_user: AuthenticatedUser,
    session: Session = Depends(get_session),
) -> TaskRead:
    """Get a single task by ID."""
    # Query with user isolation (defense in depth)
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).first()

    if not task:
        # Check if task exists but belongs to another user
        exists = session.get(Task, task_id)
        if exists:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    return TaskRead.model_validate(task)


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: AuthenticatedUser,
    session: Session = Depends(get_session),
) -> TaskRead:
    """Create a new task for the authenticated user."""
    task = Task(
        **task_data.model_dump(),
        user_id=current_user.id,
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskRead.model_validate(task)


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: AuthenticatedUser,
    session: Session = Depends(get_session),
) -> TaskRead:
    """Fully update a task (all fields required)."""
    # Query with user isolation (defense in depth)
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).first()

    if not task:
        exists = session.get(Task, task_id)
        if exists:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    # Update all fields
    for key, value in task_data.model_dump().items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskRead.model_validate(task)


@router.patch("/{task_id}", response_model=TaskRead)
def partial_update_task(
    task_id: int,
    task_data: TaskPatch,
    current_user: AuthenticatedUser,
    session: Session = Depends(get_session),
) -> TaskRead:
    """Partially update a task (only provided fields)."""
    # Query with user isolation (defense in depth)
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).first()

    if not task:
        exists = session.get(Task, task_id)
        if exists:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    # Update only provided fields
    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskRead.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: AuthenticatedUser,
    session: Session = Depends(get_session),
) -> None:
    """Delete a task."""
    # Query with user isolation (defense in depth)
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).first()

    if not task:
        exists = session.get(Task, task_id)
        if exists:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    session.delete(task)
    session.commit()

    return None
