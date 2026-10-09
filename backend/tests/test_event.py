
import pytest


def test_create_event_returns_201_with_created_event(client):
    """Test creating a valid event returns a 201 and the created event"""

    response = client.post(
        "/v1/events", json={
            "name": "Open Play",
            "description": "Open Play Description",
            "date": "2026-09-26",
            "max_players": 30
        }
    )

    data = response.json()

    assert response.status_code == 201
    assert data['data']['name'] == "Open Play"
    assert data['data']['description'] == "Open Play Description"
    assert data['data']['date'] == "2026-09-26"
    assert data['data']['maxPlayers'] == 30
    assert data['data']['createdAt'] is not None
    assert data['data']['updatedAt'] is not None


def test_missing_name(client):
    response = client.post(
        "/v1/events", json={
            "description": "Open Play Description",
            "date": "2026-09-26",
            "max_players": 30
        }
    )

    assert response.status_code >= 400 and response.status_code < 500


def test_missing_description(client):
    response = client.post(
        "/v1/events", json={
            "name": "Open Play",
            "date": "2026-09-26",
            "max_players": 30
        }
    )

    assert response.status_code >= 400 and response.status_code < 500


def test_missing_date(client):
    response = client.post(
        "/v1/events", json={
            "name": "Open Play",
            "description": "Open Play Description",
            "max_players": 30
        }
    )

    assert response.status_code >= 400 and response.status_code < 500


def test_missing_max_players(client):
    response = client.post(
        "/v1/events", json={
            "name": "Open Play",
            "description": "Open Play Description",
            "date": "2026-09-26",
        }
    )

    assert response.status_code >= 400 and response.status_code < 500


def test_invalid_date_format(client):
    response = client.post(
        "/v1/events", json={
            "name": "Open Play",
            "description": "Open Play Description",
            "date": "2026-09",
        }
    )

    assert response.status_code >= 400 and response.status_code < 500


def test_negative_max_players(client):
    response = client.post(
        "/v1/events", json={
            "name": "Open Play",
            "description": "Open Play Description",
            "date": "2026-09-26",
            "max_players": -10
        }
    )

    assert response.status_code >= 400 and response.status_code < 500


def test_above_max_players_limit(client):
    response = client.post(
        "/v1/events", json={
            "name": "Open Play",
            "description": "Open Play Description",
            "date": "2026-09-26",
            "max_players": 100
        }
    )

    assert response.status_code >= 400 and response.status_code < 500


def test_fetch_event_returns_200_and_the_event(client, event):
    response = client.get(f"/v1/events/{event.id}")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["id"] == str(event.id)
    assert data["name"] == event.name
    assert data["description"] == event.description
    assert data["date"] == event.date.isoformat()
    assert data["maxPlayers"] == event.max_players


def test_fetch_non_existent_event_returns_404(client):
    response = client.get(f"/v1/events/234ca24b905d44e3a52b4f1fa20f8742")

    assert response.status_code == 404


def test_fetch_for_invalid_event_returns_422(client):
    response = client.get(f"/v1/events/fahafa")

    assert response.status_code == 422
