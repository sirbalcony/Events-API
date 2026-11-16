import requests


# Happy path tests
def test_health_endpoint_returns_healthy(base_url):
    response = requests.get(
        f"{base_url}/api/health",
        timeout=5
    )

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_user_creates_new_user(base_url, user_data):
    response = requests.post(
        f"{base_url}/api/auth/register",
        json=user_data,
        timeout=5
    )

    assert response.status_code == 201
    assert response.json()["user"]["username"] == user_data["username"]
    assert "id" in response.json()["user"]


def test_login_returns_jwt_token(base_url, user_data):
    register_response = requests.post(
        f"{base_url}/api/auth/register",
        json=user_data,
        timeout=5
    )
    assert register_response.status_code == 201

    response = requests.post(
        f"{base_url}/api/auth/login",
        json=user_data,
        timeout=5
    )

    assert response.status_code == 200
    assert response.json()["access_token"]


def test_create_public_event_succeeds_with_token(
    base_url, auth_token, event_data
):
    response = requests.post(
        f"{base_url}/api/events",
        json=event_data,
        headers={"Authorization": f"Bearer {auth_token}"},
        timeout=5
    )

    assert response.status_code == 201
    assert response.json()["title"] == event_data["title"]
    assert response.json()["date"] == event_data["date"]
    assert response.json()["is_public"] is True


def test_public_event_rsvp_without_auth(
    base_url, auth_token, event_data
):
    event_response = requests.post(
        f"{base_url}/api/events",
        json=event_data,
        headers={"Authorization": f"Bearer {auth_token}"},
        timeout=5
    )
    assert event_response.status_code == 201

    event_id = event_response.json()["id"]

    response = requests.post(
        f"{base_url}/api/rsvps/event/{event_id}",
        json={"attending": True},
        timeout=5
    )

    assert response.status_code == 201
    assert response.json()["event_id"] == event_id
    assert response.json()["attending"] is True
    assert response.json()["user_id"] is None


# Error and edge case tests
def test_duplicate_registration_returns_400(base_url, user_data):
    first_response = requests.post(
        f"{base_url}/api/auth/register",
        json=user_data,
        timeout=5
    )
    assert first_response.status_code == 201

    second_response = requests.post(
        f"{base_url}/api/auth/register",
        json=user_data,
        timeout=5
    )

    assert second_response.status_code == 400
    assert second_response.json()["error"] == "Username already exists"


def test_create_event_without_auth_returns_401(base_url, event_data):
    response = requests.post(
        f"{base_url}/api/events",
        json=event_data,
        timeout=5
    )

    assert response.status_code == 401
    assert response.json()["msg"] == "Missing Authorization Header"


def test_private_event_rsvp_without_auth_returns_401(
    base_url, auth_token, event_data
):
    event_data["is_public"] = False

    event_response = requests.post(
        f"{base_url}/api/events",
        json=event_data,
        headers={"Authorization": f"Bearer {auth_token}"},
        timeout=5
    )
    assert event_response.status_code == 201

    event_id = event_response.json()["id"]

    response = requests.post(
        f"{base_url}/api/rsvps/event/{event_id}",
        json={"attending": True},
        timeout=5
    )

    assert response.status_code == 401
    assert response.json()["error"] == (
        "Authentication required for this event"
    )