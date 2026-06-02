from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "status": "running",
        "service": "Cost Finance AI Agent",
        "environment": "development"
    }

def test_response_includes_request_id_header():
    response = client.get("/")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers


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

def test_budget_comparison_endpoint_returns_budget_status():
    response = client.get("/api/v1/budget-comparison/1")

    assert response.status_code == 200
    assert response.json() == {
        "subsystem": "Foundation",
        "planned_cost": 50000,
        "actual_cost": 42000,
        "variance": 8000,
        "budget_status": "under_budget"
    }

def test_overrun_risk_endpoint_returns_risk_level():
    response = client.get("/api/v1/overrun-risk/1")

    assert response.status_code == 200
    assert response.json() == {
        "subsystem": "Foundation",
        "planned_cost": 50000,
        "actual_cost": 42000,
        "utilization_percent": 84.0,
        "risk_level": "medium"
    }

def test_financial_summary_endpoint_returns_all_sections():
    response = client.get("/api/v1/financial-summary/1")

    assert response.status_code == 200

    data = response.json()

    assert data["subsystem"] == "Foundation"
    assert data["cost"]["remaining_budget"] == 8000
    assert data["breakdown"]["labor_cost"] == 15000
    assert data["budget_comparison"]["budget_status"] == "under_budget"
    assert data["overrun_risk"]["risk_level"] == "medium"

def test_cost_endpoint_returns_404_for_unknown_subsystem():
    response = client.get("/api/v1/costs/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Subsystem not found"
    }

def test_budget_comparison_endpoint_returns_404_for_unknown_subsystem():
    response = client.get("/api/v1/budget-comparison/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Subsystem not found"
    }
def test_overrun_risk_endpoint_returns_404_for_unknown_subsystem():
    response = client.get("/api/v1/overrun-risk/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Subsystem not found"
    }
def test_financial_summary_endpoint_returns_404_for_unknown_subsystem():
    response = client.get("/api/v1/financial-summary/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Subsystem not found"
    }

def test_global_exception_handler_returns_consistent_error_response():
    error_client = TestClient(app, raise_server_exceptions=False)

    @app.get("/test-error")
    def test_error():
        raise RuntimeError("Boom")

    response = error_client.get("/test-error")

    assert response.status_code == 500
    assert response.json() == {
        "status": "error",
        "message": "Internal server error"
    }