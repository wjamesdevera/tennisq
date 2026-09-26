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
    assert data['event']['name'] == "Open Play"
    assert data['event']['description'] == "Open Play Description"
    assert data['event']['date'] == "2026-09-26"
    assert data['event']['max_players'] == 30
    assert data['event']['created_at'] is not None
    assert data['event']['updated_at'] is not None
