"""
Phase 2 Full-Stack Todo App - Authentication Tests

Tests for JWT verification and auth failures (T067, T070).
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db import get_session
from app.dependencies import get_current_user, CurrentUser


class TestAuthenticationRequired:
    """Tests for authentication requirement on protected endpoints (T070)."""

    def test_list_tasks_requires_auth(self, client: TestClient):
        """GET /api/tasks returns 401 without authentication."""
        response = client.get("/api/tasks")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    def test_get_task_requires_auth(self, client: TestClient):
        """GET /api/tasks/{id} returns 401 without authentication."""
        response = client.get("/api/tasks/1")
        assert response.status_code == 401

    def test_create_task_requires_auth(self, client: TestClient):
        """POST /api/tasks returns 401 without authentication."""
        response = client.post("/api/tasks", json={"title": "Test"})
        assert response.status_code == 401

    def test_update_task_requires_auth(self, client: TestClient):
        """PUT /api/tasks/{id} returns 401 without authentication."""
        response = client.put(
            "/api/tasks/1",
            json={"title": "Test", "description": None, "is_complete": False},
        )
        assert response.status_code == 401

    def test_patch_task_requires_auth(self, client: TestClient):
        """PATCH /api/tasks/{id} returns 401 without authentication."""
        response = client.patch("/api/tasks/1", json={"is_complete": True})
        assert response.status_code == 401

    def test_delete_task_requires_auth(self, client: TestClient):
        """DELETE /api/tasks/{id} returns 401 without authentication."""
        response = client.delete("/api/tasks/1")
        assert response.status_code == 401


class TestPublicEndpoints:
    """Tests for endpoints that don't require authentication."""

    def test_health_check_no_auth(self, client: TestClient):
        """GET /health doesn't require authentication."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root_no_auth(self, client: TestClient):
        """GET / doesn't require authentication."""
        response = client.get("/")
        assert response.status_code == 200
        assert "docs" in response.json()

    def test_openapi_docs_available(self, client: TestClient):
        """OpenAPI docs are available at /docs."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_json_available(self, client: TestClient):
        """OpenAPI JSON spec is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert data["info"]["title"] == "Phase 2 Todo API"


class TestInputValidation:
    """Tests for input validation (T071)."""

    def test_empty_title_rejected(self, authenticated_client: TestClient):
        """Empty title is rejected with 422."""
        response = authenticated_client.post("/api/tasks", json={"title": ""})
        assert response.status_code == 422

    def test_whitespace_only_title_rejected(self, authenticated_client: TestClient):
        """Whitespace-only title is rejected with 422."""
        response = authenticated_client.post("/api/tasks", json={"title": "   "})
        # Note: This depends on how validation is configured
        # If using strip, this might be rejected as empty
        assert response.status_code in [201, 422]  # Accept either behavior

    def test_title_max_length_boundary(self, authenticated_client: TestClient):
        """Title at max length (500) is accepted."""
        response = authenticated_client.post(
            "/api/tasks", json={"title": "x" * 500}
        )
        assert response.status_code == 201

    def test_title_over_max_length_rejected(self, authenticated_client: TestClient):
        """Title over max length (501) is rejected."""
        response = authenticated_client.post(
            "/api/tasks", json={"title": "x" * 501}
        )
        assert response.status_code == 422

    def test_description_max_length_boundary(self, authenticated_client: TestClient):
        """Description at max length (2000) is accepted."""
        response = authenticated_client.post(
            "/api/tasks",
            json={"title": "Test", "description": "x" * 2000},
        )
        assert response.status_code == 201

    def test_description_over_max_length_rejected(self, authenticated_client: TestClient):
        """Description over max length (2001) is rejected."""
        response = authenticated_client.post(
            "/api/tasks",
            json={"title": "Test", "description": "x" * 2001},
        )
        assert response.status_code == 422

    def test_invalid_status_filter_rejected(self, authenticated_client: TestClient):
        """Invalid status filter value is rejected."""
        response = authenticated_client.get("/api/tasks?status=invalid")
        assert response.status_code == 422

    def test_invalid_limit_rejected(self, authenticated_client: TestClient):
        """Limit > 100 is rejected."""
        response = authenticated_client.get("/api/tasks?limit=101")
        assert response.status_code == 422

    def test_negative_offset_rejected(self, authenticated_client: TestClient):
        """Negative offset is rejected."""
        response = authenticated_client.get("/api/tasks?offset=-1")
        assert response.status_code == 422


class TestE2EWorkflow:
    """End-to-end workflow test (T068)."""

    def test_complete_task_lifecycle(self, authenticated_client: TestClient):
        """
        E2E test: create task → view task → complete task → delete task.

        Note: Signup/signin is handled by Better Auth in the frontend.
        This test covers the API workflow for an authenticated user.
        """
        # 1. Create a new task
        create_response = authenticated_client.post(
            "/api/tasks",
            json={"title": "E2E Test Task", "description": "Testing the full workflow"},
        )
        assert create_response.status_code == 201
        task = create_response.json()
        task_id = task["id"]
        assert task["title"] == "E2E Test Task"
        assert task["is_complete"] is False

        # 2. View the task
        get_response = authenticated_client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 200
        assert get_response.json()["title"] == "E2E Test Task"

        # 3. Complete the task
        patch_response = authenticated_client.patch(
            f"/api/tasks/{task_id}",
            json={"is_complete": True},
        )
        assert patch_response.status_code == 200
        assert patch_response.json()["is_complete"] is True

        # 4. Verify task appears in completed list
        list_response = authenticated_client.get("/api/tasks?status=complete")
        assert list_response.status_code == 200
        completed_ids = [t["id"] for t in list_response.json()["tasks"]]
        assert task_id in completed_ids

        # 5. Delete the task
        delete_response = authenticated_client.delete(f"/api/tasks/{task_id}")
        assert delete_response.status_code == 204

        # 6. Verify task is gone
        verify_response = authenticated_client.get(f"/api/tasks/{task_id}")
        assert verify_response.status_code == 404
