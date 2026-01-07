"""
Phase 2 Full-Stack Todo App - Test Configuration

Pytest fixtures for API integration tests.
"""

import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.db import get_session
from app.dependencies import get_current_user, CurrentUser
from app.models import Task


# Test database URL (in-memory SQLite for tests)
TEST_DATABASE_URL = "sqlite://"


@pytest.fixture(name="engine")
def engine_fixture():
    """Create a test database engine."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="session")
def session_fixture(engine) -> Generator[Session, None, None]:
    """Create a test database session."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database session override."""

    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


# Test users
TEST_USER_A = CurrentUser(id="user_a_123", email="usera@example.com")
TEST_USER_B = CurrentUser(id="user_b_456", email="userb@example.com")


@pytest.fixture(name="authenticated_client")
def authenticated_client_fixture(session: Session) -> Generator[TestClient, None, None]:
    """Create a test client authenticated as User A."""

    def get_session_override():
        yield session

    def get_current_user_override():
        return TEST_USER_A

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = get_current_user_override

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(name="authenticated_client_user_b")
def authenticated_client_user_b_fixture(session: Session) -> Generator[TestClient, None, None]:
    """Create a test client authenticated as User B."""

    def get_session_override():
        yield session

    def get_current_user_override():
        return TEST_USER_B

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = get_current_user_override

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(name="sample_task")
def sample_task_fixture(session: Session) -> Task:
    """Create a sample task for User A."""
    task = Task(
        title="Test Task",
        description="Test description",
        is_complete=False,
        user_id=TEST_USER_A.id,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@pytest.fixture(name="sample_tasks")
def sample_tasks_fixture(session: Session) -> list[Task]:
    """Create multiple sample tasks for User A."""
    tasks = [
        Task(title="Task 1", description="Description 1", is_complete=False, user_id=TEST_USER_A.id),
        Task(title="Task 2", description="Description 2", is_complete=True, user_id=TEST_USER_A.id),
        Task(title="Task 3", description=None, is_complete=False, user_id=TEST_USER_A.id),
    ]
    for task in tasks:
        session.add(task)
    session.commit()
    for task in tasks:
        session.refresh(task)
    return tasks


@pytest.fixture(name="user_b_task")
def user_b_task_fixture(session: Session) -> Task:
    """Create a task owned by User B."""
    task = Task(
        title="User B Task",
        description="Belongs to User B",
        is_complete=False,
        user_id=TEST_USER_B.id,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
