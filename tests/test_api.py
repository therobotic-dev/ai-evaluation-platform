
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_evaluations():
    response = client.get("/evaluations/")

    assert response.status_code == 200
    assert "data" in response.json()
    assert "total" in response.json()


def test_get_rubrics():
    response = client.get("/rubrics/")

    assert response.status_code == 200
    assert "data" in response.json()
    assert "total" in response.json()


def test_get_analytics_summary():
    response = client.get("/analytics/summary")

    assert response.status_code == 200
    assert "total_evaluations" in response.json()
    assert "status_summary" in response.json()
    assert "average_score" in response.json()


def test_get_disagreements():
    response = client.get("/disagreements/")

    assert response.status_code == 200
    assert "data" in response.json()
    assert "total" in response.json()


def test_get_audit_logs():
    response = client.get("/audit-logs/")

    assert response.status_code == 200
    assert "data" in response.json()
    assert "total" in response.json()


def test_dashboard_endpoint():
    response = client.get("/dashboard")

    assert response.status_code == 200
    assert "AI Evaluation Quality Dashboard" in response.text
