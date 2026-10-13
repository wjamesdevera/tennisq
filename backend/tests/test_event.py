
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


@pytest.mark.parametrize("payload, bad_field", [
    (
        {
            "description": "Open Play Description",
            "date": "2026-09-26",
            "maxPlayers": 30
        },
        "name"
    ),  # missing name
    (
        {
            "name": "Open Play",
            "date": "2026-09-26",
            "maxPlayers": 30
        },
        "description"
    ),  # missing description
    (
        {
            "name": "Open Play",
            "description": "Open Play Description",
            "maxPlayers": 30
        },
        "date"
    ),  # missing date
    (
        {
            "name": "Open Play",
            "description": "Open Play Description",
            "date": "2026-09-26",
        },
        "maxPlayers"
    ),  # missing max_players
    (
        {
            "name": "Open Play",
            "description": "Open Play Description",
            "maxPlayers": 30,
            "date": "2026-09",
        },
        "date"
    ),  # invalid date format
    (
        {
            "name": "Open Play",
            "description": "Open Play Description",
            "date": "2026-09-26",
            "maxPlayers": -10
        },
        "maxPlayers"
    ),  # negative max players
    (
        {
            "name": "Open Play",
            "description": "Open Play Description",
            "date": "2026-09-26",
            "maxPlayers": 100
        },
        "maxPlayers"
    ),  # above max_players limit
])
def test_create_event_with_invalid_payload_returns_422(client, payload, bad_field):
    response = client.post("v1/events", json=payload)

    assert response.status_code == 422
    assert bad_field in [err for part in response.json()['detail']
                         for err in part['loc']]


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


def test_fetch_event_players_returns_200_and_a_list_of_players(client, event):
    response = client.get(f'/v1/events/{event.id}/players')

    assert response.status_code == 200
    data = response.json()['data']
    assert data['total'] == 40
    assert data['limit'] == 20
    assert data['offset'] == 0


@pytest.mark.parametrize("limit, offset, expected", [
    (20, 0, {"limit": 20, "offset": 0}),
    (20, 20, {"limit": 20, "offset": 20}),
])
def test_fetch_event_players_returns_200_and_a_list_of_players(client, event, limit, offset, expected):
    response = client.get(
        f'/v1/events/{event.id}/players?limit={limit}&offset={offset}')

    assert response.status_code == 200
    data = response.json()['data']
    assert data['total'] == 40
    assert data['limit'] == expected['limit']
    assert data['offset'] == expected['offset']
