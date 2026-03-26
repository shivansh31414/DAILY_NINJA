import os
import requests


BASE_URL = os.getenv("DAILY_NINJA_BASE_URL", "https://daily-ninja-app.azurewebsites.net").rstrip("/")


def test_health_endpoint():
    response = requests.get(f"{BASE_URL}/health", timeout=15)
    assert response.status_code == 200
    payload = response.json()
    assert payload.get("status") == "healthy"


def test_root_endpoint():
    response = requests.get(f"{BASE_URL}/", timeout=15)
    assert response.status_code == 200
    payload = response.json()
    assert "service" in payload
    assert "endpoints" in payload


def test_tasks_endpoint_requires_auth_or_returns_ok():
    response = requests.get(f"{BASE_URL}/tasks", timeout=15)
    assert response.status_code in (200, 401)
