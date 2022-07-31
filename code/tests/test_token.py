import logging
import random
from urllib import response

import app.core.config as config
import app.main as main
import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

LOGGER = logging.getLogger(__name__)

client = TestClient(main.app)

EMAIL = "nuomlhhnyg@example.com"


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


def create_user(email: str):
    response = client.post(
        "/api/v1/user",
        json={
            "email": email,
            "is_active": False,
            "full_name": "test",
            "password": "test",
        },
    )
    return response


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

    # Check if the response contains the access token
    assert "access_token" in response.json()
    assert "token_type" in response.json()

    # Use the access token to access the protected endpoint
    bearer = f"Bearer {response.json()['access_token']}"
    client.headers["Authorization"] = bearer
    response = client.post("/api/v1/login/test-token")

    # Try to validate the email with a bad token
    client.headers["Authorization"] = "Bearer bad_token"
    response = client.post("/api/v1/login/email-validator")
    assert response.status_code == 403

    # Get the email validator
    client.headers["Authorization"] = bearer
    response = client.post("/api/v1/login/email-validator")
    assert response.status_code == 200

    # Validate the email

    email_code = response.json()["email_code"]
    assert email_code is not None

    LOGGER.critical(email_code)

    # Validate with token-validator that take as input the email code
    client.headers["Authorization"] = bearer
    # response = client.post("api/v1/login/token-validator?token=" + email_code)
    LOGGER.critical(response.content)
    # assert response.status_code == 200


# Try to get email with a bad token
def test_get_email_with_bad_token():
    client.headers["Authorization"] = "Bearer bad_token"
    response = client.post("/api/v1/login/test-token")
    assert response.status_code == 403
