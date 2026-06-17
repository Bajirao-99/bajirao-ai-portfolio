from fastapi.testclient import TestClient

from app.main import app


client = TestClient(
    app,
    base_url="http://localhost",
)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert (
        response.json()["status"]
        == "success"
    )


def test_health_endpoint():
    response = client.get(
        "/api/v1/health"
    )

    assert response.status_code == 200
    assert (
        response.json()["status"]
        == "healthy"
    )


def test_admin_analytics_requires_login():
    response = client.get(
        "/api/v1/admin/analytics"
    )

    assert response.status_code == 401


def test_invalid_contact_message():
    response = client.post(
        "/api/v1/contact",
        json={
            "name": "A",
            "email": "invalid-email",
            "subject": "Hi",
            "message": "Short",
        },
    )

    assert response.status_code == 422


def test_invalid_job_description():
    response = client.post(
        "/api/v1/ai/job-match",
        json={
            "job_description": "Too short",
            "top_k": 3,
        },
    )

    assert response.status_code == 422