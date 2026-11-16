from uuid import uuid4

import pytest
import requests


BASE_URL = "http://localhost:5000"


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def user_data():
    return {
        "username": f"test_{uuid4().hex[:12]}",
        "password": "Testpassword123!"
    }


@pytest.fixture
def auth_token(base_url, user_data):
    response = requests.post(
        f"{base_url}/api/auth/register",
        json=user_data,
        timeout=5
    )
    assert response.status_code == 201

    response = requests.post(
        f"{base_url}/api/auth/login",
        json=user_data,
        timeout=5
    )
    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture
def event_data():
    return {
        "title": "Masterschool Test Event",
        "description": "Event created during API testing",
        "date": "2027-01-15T18:00:00",
        "location": "Online",
        "capacity": 10,
        "is_public": True,
        "requires_admin": False
    }