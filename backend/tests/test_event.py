def test_create_event(client):

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
    assert data['data']['max_players'] == 30
    assert data['data']['created_at'] is not None
    assert data['data']['updated_at'] is not None


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
