"""
Phase 2 Full-Stack Todo App - Task API Integration Tests

Tests for all task CRUD endpoints with user isolation.
"""

import pytest
from fastapi.testclient import TestClient

from app.models import Task


class TestListTasks:
    """Tests for GET /api/tasks endpoint."""

    def test_list_tasks_empty(self, authenticated_client: TestClient):
        """Returns empty list when user has no tasks."""
        response = authenticated_client.get("/api/tasks")
        assert response.status_code == 200
        data = response.json()
        assert data["tasks"] == []
        assert data["total"] == 0

    def test_list_tasks_returns_user_tasks(
        self, authenticated_client: TestClient, sample_tasks: list[Task]
    ):
        """Returns only the authenticated user's tasks."""
        response = authenticated_client.get("/api/tasks")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["tasks"]) == 3

    def test_list_tasks_filter_complete(
        self, authenticated_client: TestClient, sample_tasks: list[Task]
    ):
        """Filters tasks by completion status."""
        response = authenticated_client.get("/api/tasks?status=complete")
        assert response.status_code == 200
        data = response.json()
        assert all(task["is_complete"] for task in data["tasks"])

    def test_list_tasks_filter_pending(
        self, authenticated_client: TestClient, sample_tasks: list[Task]
    ):
        """Filters tasks by pending status."""
        response = authenticated_client.get("/api/tasks?status=pending")
        assert response.status_code == 200
        data = response.json()
        assert all(not task["is_complete"] for task in data["tasks"])

    def test_list_tasks_pagination(
        self, authenticated_client: TestClient, sample_tasks: list[Task]
    ):
        """Supports pagination with limit and offset."""
        response = authenticated_client.get("/api/tasks?limit=2&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 2
        assert data["limit"] == 2
        assert data["offset"] == 0

    def test_list_tasks_user_isolation(
        self,
        authenticated_client: TestClient,
        sample_task: Task,
        user_b_task: Task,
    ):
        """User A cannot see User B's tasks."""
        response = authenticated_client.get("/api/tasks")
        assert response.status_code == 200
        data = response.json()
        task_ids = [task["id"] for task in data["tasks"]]
        assert sample_task.id in task_ids
        assert user_b_task.id not in task_ids


class TestGetTask:
    """Tests for GET /api/tasks/{task_id} endpoint."""

    def test_get_task_success(
        self, authenticated_client: TestClient, sample_task: Task
    ):
        """Returns a task by ID."""
        response = authenticated_client.get(f"/api/tasks/{sample_task.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_task.id
        assert data["title"] == sample_task.title

    def test_get_task_not_found(self, authenticated_client: TestClient):
        """Returns 404 for non-existent task."""
        response = authenticated_client.get("/api/tasks/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_task_forbidden(
        self, authenticated_client: TestClient, user_b_task: Task
    ):
        """Returns 403 when accessing another user's task."""
        response = authenticated_client.get(f"/api/tasks/{user_b_task.id}")
        assert response.status_code == 403
        assert response.json()["detail"] == "Access denied"


class TestCreateTask:
    """Tests for POST /api/tasks endpoint."""

    def test_create_task_success(self, authenticated_client: TestClient):
        """Creates a new task."""
        response = authenticated_client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "New description"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Task"
        assert data["description"] == "New description"
        assert data["is_complete"] is False
        assert "id" in data

    def test_create_task_minimal(self, authenticated_client: TestClient):
        """Creates a task with only required fields."""
        response = authenticated_client.post(
            "/api/tasks",
            json={"title": "Minimal Task"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minimal Task"
        assert data["description"] is None

    def test_create_task_empty_title_rejected(self, authenticated_client: TestClient):
        """Rejects task with empty title."""
        response = authenticated_client.post(
            "/api/tasks",
            json={"title": ""},
        )
        assert response.status_code == 422

    def test_create_task_title_too_long(self, authenticated_client: TestClient):
        """Rejects task with title exceeding 500 characters."""
        response = authenticated_client.post(
            "/api/tasks",
            json={"title": "x" * 501},
        )
        assert response.status_code == 422

    def test_create_task_description_too_long(self, authenticated_client: TestClient):
        """Rejects task with description exceeding 2000 characters."""
        response = authenticated_client.post(
            "/api/tasks",
            json={"title": "Valid Title", "description": "x" * 2001},
        )
        assert response.status_code == 422


class TestUpdateTask:
    """Tests for PUT /api/tasks/{task_id} endpoint."""

    def test_update_task_success(
        self, authenticated_client: TestClient, sample_task: Task
    ):
        """Updates a task with all fields."""
        response = authenticated_client.put(
            f"/api/tasks/{sample_task.id}",
            json={
                "title": "Updated Title",
                "description": "Updated description",
                "is_complete": True,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated description"
        assert data["is_complete"] is True

    def test_update_task_not_found(self, authenticated_client: TestClient):
        """Returns 404 for non-existent task."""
        response = authenticated_client.put(
            "/api/tasks/99999",
            json={"title": "Updated", "description": None, "is_complete": False},
        )
        assert response.status_code == 404

    def test_update_task_forbidden(
        self, authenticated_client: TestClient, user_b_task: Task
    ):
        """Returns 403 when updating another user's task."""
        response = authenticated_client.put(
            f"/api/tasks/{user_b_task.id}",
            json={"title": "Hacked", "description": None, "is_complete": False},
        )
        assert response.status_code == 403


class TestPatchTask:
    """Tests for PATCH /api/tasks/{task_id} endpoint."""

    def test_patch_task_toggle_complete(
        self, authenticated_client: TestClient, sample_task: Task
    ):
        """Toggles task completion status."""
        response = authenticated_client.patch(
            f"/api/tasks/{sample_task.id}",
            json={"is_complete": True},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_complete"] is True
        assert data["title"] == sample_task.title  # Other fields unchanged

    def test_patch_task_update_title_only(
        self, authenticated_client: TestClient, sample_task: Task
    ):
        """Updates only the title."""
        response = authenticated_client.patch(
            f"/api/tasks/{sample_task.id}",
            json={"title": "New Title Only"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title Only"
        assert data["description"] == sample_task.description

    def test_patch_task_not_found(self, authenticated_client: TestClient):
        """Returns 404 for non-existent task."""
        response = authenticated_client.patch(
            "/api/tasks/99999",
            json={"is_complete": True},
        )
        assert response.status_code == 404

    def test_patch_task_forbidden(
        self, authenticated_client: TestClient, user_b_task: Task
    ):
        """Returns 403 when patching another user's task."""
        response = authenticated_client.patch(
            f"/api/tasks/{user_b_task.id}",
            json={"is_complete": True},
        )
        assert response.status_code == 403


class TestDeleteTask:
    """Tests for DELETE /api/tasks/{task_id} endpoint."""

    def test_delete_task_success(
        self, authenticated_client: TestClient, sample_task: Task
    ):
        """Deletes a task."""
        response = authenticated_client.delete(f"/api/tasks/{sample_task.id}")
        assert response.status_code == 204

        # Verify task is deleted
        response = authenticated_client.get(f"/api/tasks/{sample_task.id}")
        assert response.status_code == 404

    def test_delete_task_not_found(self, authenticated_client: TestClient):
        """Returns 404 for non-existent task."""
        response = authenticated_client.delete("/api/tasks/99999")
        assert response.status_code == 404

    def test_delete_task_forbidden(
        self, authenticated_client: TestClient, user_b_task: Task
    ):
        """Returns 403 when deleting another user's task."""
        response = authenticated_client.delete(f"/api/tasks/{user_b_task.id}")
        assert response.status_code == 403


class TestUserIsolation:
    """Tests for user isolation (T069)."""

    def test_user_a_cannot_see_user_b_tasks(
        self,
        authenticated_client: TestClient,
        authenticated_client_user_b: TestClient,
        sample_task: Task,
        user_b_task: Task,
    ):
        """User A only sees their own tasks."""
        # User A's view
        response_a = authenticated_client.get("/api/tasks")
        task_ids_a = [t["id"] for t in response_a.json()["tasks"]]
        assert sample_task.id in task_ids_a
        assert user_b_task.id not in task_ids_a

        # User B's view
        response_b = authenticated_client_user_b.get("/api/tasks")
        task_ids_b = [t["id"] for t in response_b.json()["tasks"]]
        assert user_b_task.id in task_ids_b
        assert sample_task.id not in task_ids_b

    def test_user_a_cannot_access_user_b_task_by_id(
        self, authenticated_client: TestClient, user_b_task: Task
    ):
        """User A gets 403 when trying to access User B's task."""
        response = authenticated_client.get(f"/api/tasks/{user_b_task.id}")
        assert response.status_code == 403

    def test_user_a_cannot_modify_user_b_task(
        self, authenticated_client: TestClient, user_b_task: Task
    ):
        """User A gets 403 when trying to modify User B's task."""
        # PUT
        response = authenticated_client.put(
            f"/api/tasks/{user_b_task.id}",
            json={"title": "Hacked", "description": None, "is_complete": True},
        )
        assert response.status_code == 403

        # PATCH
        response = authenticated_client.patch(
            f"/api/tasks/{user_b_task.id}",
            json={"is_complete": True},
        )
        assert response.status_code == 403

        # DELETE
        response = authenticated_client.delete(f"/api/tasks/{user_b_task.id}")
        assert response.status_code == 403
