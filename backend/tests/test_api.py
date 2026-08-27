import os

os.environ.setdefault(
    "FAMILYGUARD_DATABASE_URL",
    "sqlite:///./test_familyguard.db",
)

from fastapi.testclient import TestClient  # noqa: E402

from backend.main import app  # noqa: E402


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_children_contains_seeded_child() -> None:
    with TestClient(app) as client:
        response = client.get("/children")

    assert response.status_code == 200
    data = response.json()
    assert data
    assert data[0]["name"] == "Alex"


def test_child_check_in_updates_shared_state() -> None:
    payload = {
        "status": "On my way home",
        "location_label": "Library",
        "battery_percent": 61,
    }

    with TestClient(app) as client:
        response = client.post("/children/1/check-in", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == payload["status"]
    assert data["location_label"] == payload["location_label"]
    assert data["battery_percent"] == payload["battery_percent"]


def test_usage_validation_rejects_impossible_screen_time() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/children/1/usage",
            json={"screen_time_minutes": 1500, "top_apps": []},
        )

    assert response.status_code == 422


def test_unknown_child_returns_404() -> None:
    with TestClient(app) as client:
        response = client.get("/children/999")

    assert response.status_code == 404
