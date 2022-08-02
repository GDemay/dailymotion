import logging
import random

import pytest
from starlette.testclient import TestClient

import app.main as main
from app.core.config import settings
from app.core.email import Email
from tests.utils import RANDOM_EMAIL, USER_ID, authenticate_user, client

LOGGER = logging.getLogger(__name__)


def test_user_can_login_successfully_and_receives_valid_token() -> None:

    response = authenticate_user(email=RANDOM_EMAIL, password="test")
    assert response.status_code == 200

    # Check if the response contains the access token
    assert "access_token" in response.json()
    assert "token_type" in response.json()

    # Use the access token to access the protected endpoint
    client.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    response = client.post(f"{settings.API_VERSION}/login/me")
    assert response.status_code == 200


# Connect with a bad password
def test_authenticate_user_with_bad_password():
    response = authenticate_user(email=RANDOM_EMAIL, password="bad_password")
    assert response.status_code == 401


# Get a email-valitor with a bad token
def test_get_email_validator():

    response = authenticate_user(email=RANDOM_EMAIL, password="test")
    assert response.status_code == 200

    # Check if the response contains the access token
    assert "access_token" in response.json()
    assert "token_type" in response.json()

    # Use the access token to access the protected endpoint
    bearer = f"Bearer {response.json()['access_token']}"
    client.headers["Authorization"] = bearer
    response = client.post(f"{settings.API_VERSION}/login/me")

    # Try to validate the email with a bad token
    client.headers["Authorization"] = "Bearer bad_token"
    response = client.post(f"{settings.API_VERSION}/login/verify-email")
    assert response.status_code == 403

    # Get the email validator
    client.headers["Authorization"] = bearer
    response = client.post(f"{settings.API_VERSION}/login/verify-email")
    assert response.status_code == 200

    # Validate the email

    email_code = response.json()["email_code"]
    assert email_code is not None

    LOGGER.critical(email_code)

    # Validate with activate-user that take as input the email code
    client.headers["Authorization"] = bearer
    # response = client.post("api/v1/login/activate-user?token=" + email_code)
    LOGGER.critical(response.content)
    # assert response.status_code == 200


# Try to get email with a bad token
def test_get_email_with_bad_token():
    client.headers["Authorization"] = "Bearer bad_token"
    response = client.post(f"{settings.API_VERSION}/login/me")
    assert response.status_code == 403


def test_mailgun_api_key_set():
    assert settings.MAILJET_API_KEY is not None


def test_send_email():
    # Instantiate the Email class
    email = Email(to=RANDOM_EMAIL, text="This is the text of the email")
    Token = email.send()
    assert Token is not None
