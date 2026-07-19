from fastapi.testclient import TestClient

from app.main import app
from app.services import auth_service


client = TestClient(app)


def setup_function():
    auth_service.reset_users()


def test_signup_and_login_flow():
    signup_payload = {
        "username": "jane",
        "email": "jane@example.com",
        "password": "secret123",
    }

    signup_response = client.post("/auth/signup", json=signup_payload)
    assert signup_response.status_code == 201
    assert signup_response.json()["message"] == "User registered successfully"

    login_response = client.post(
        "/auth/login",
        json={"email": "jane@example.com", "password": "secret123"},
    )
    assert login_response.status_code == 200
    assert login_response.json()["access_token"]
