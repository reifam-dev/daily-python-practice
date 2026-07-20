"""Day 100 - Milestone: Deals Platform API - Tests.

Minimal smoke tests so the CI pytest step verifies real behaviour
rather than reporting zero tests collected.
"""
from fastapi.testclient import TestClient

from day100_deals_platform_api import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_deals_returns_list() -> None:
    response = client.get("/deals")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_investor() -> None:
    response = client.post("/investors", json={"name": "Test Fund"})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Fund"