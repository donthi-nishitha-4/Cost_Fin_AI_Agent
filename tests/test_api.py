from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "status": "running",
        "service": "Cost Finance AI Agent"
    }


def test_cost_endpoint_returns_subsystem_cost():
    response = client.get("/api/v1/costs/1")

    assert response.status_code == 200
    assert response.json()["subsystem"] == "Foundation"
    assert response.json()["remaining_budget"] == 8000


def test_breakdown_endpoint_returns_cost_breakdown():
    response = client.get("/api/v1/breakdown/2")

    assert response.status_code == 200
    assert response.json()["subsystem"] == "Electrical"
    assert response.json()["material_cost"] == 35000


def test_cost_endpoint_returns_404_for_unknown_subsystem():
    response = client.get("/api/v1/costs/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Subsystem not found"
    }
