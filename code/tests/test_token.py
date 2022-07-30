import app.main as main
import app.core.config as config
import pytest
import random
from starlette.testclient import TestClient
from fastapi import FastAPI

client = TestClient(main.app)

EMAIL = "yiickgbotj@example.com"


def authenticate_user(email: str, password: str) -> str:
    client.headers["content-type"] = "application/x-www-form-urlencoded"
    login_data = {
        "username": email,
        "password": password,
    }
    return client.post("/api/v1/login/access-token", data=login_data)


def generate_random_email():
    return (
        "".join([random.choice("abcdefghijklmnopqrstuvwxyz") for i in range(10)])
        + "@example.com"
    )


def test_user_can_login_successfully_and_receives_valid_token() -> None:

    response = authenticate_user(email=EMAIL, password="test")
    assert response.status_code == 200

    # Check if the response contains the access token
    assert "access_token" in response.json()
    assert "token_type" in response.json()

    # Use the access token to access the protected endpoint
    client.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    response = client.post("/api/v1/login/test-token")
    assert response.status_code == 200


# Connect with a bad password
def test_authenticate_user_with_bad_password():
    response = authenticate_user(email=EMAIL, password="bad_password")
    assert response.status_code == 400


# Get a email-valitor with a bad token
def test_get_email_validator():

    response = authenticate_user(email=EMAIL, password="test")
    assert response.status_code == 200

    # Get the token
    client.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    response = client.post("/api/v1/login/email-validator")

    assert response.status_code == 200

    # Get the token code from response

    token = response.json()["token"]
    assert token is not None

    # Validate the token code

    response = client.post("/api/v1/login/token-validator", data={"token": token})
    assert response.status_code == 200


# Try to get email with a bad token
def test_get_email_with_bad_token():
    client.headers["Authorization"] = "Bearer bad_token"
    response = client.post("/api/v1/login/test-token")
    assert response.status_code == 403
