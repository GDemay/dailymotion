import random

import pytest
from starlette.testclient import TestClient

import app.main as main
from app.core.config import settings
from app.core.email import Email
from tests.utils import RANDOM_EMAIL, USER_ID, client


def test_get_all_users():
    response = client.get(f"{settings.API_VERSION}/user")
    assert response.status_code == 200
    return response.json()


# Create a user
def test_create_user():
    # Create a user
    response = client.post(
        f"{settings.API_VERSION}/user",
        json={
            "email": RANDOM_EMAIL,
            "is_active": False,
            "password": "test",
        },
    )
    assert response.status_code == 200

    # Get the user
    # Get user_id
    USER_ID = response.json()["id"]
    response = client.get(f"{settings.API_VERSION}/user/{USER_ID}")
    assert response.status_code == 200


# Create a user with an invalid email
def test_create_user_invalid_email():
    # Create a user
    response = client.post(
        f"{settings.API_VERSION}/user",
        json={
            "email": "invalid_email",
            "is_active": False,
            "password": "test",
        },
    )
    assert response.status_code == 422


# Get a wrong user with an invalid id
def test_get_user_invalid_id():
    response = client.get(f"{settings.API_VERSION}/user/0")
    assert response.status_code == 404


# Search the email of the user
def test_email_in_database():
    response = client.get(f"{settings.API_VERSION}/user/email/{RANDOM_EMAIL}")
    assert response.status_code == 200


# Search a wrong email
def test_email_not_in_database():
    fake_email = "this_is_a_bad_email@example.com"
    response = client.get(f"{settings.API_VERSION}/user/email/{fake_email}")
    assert response.status_code == 404


def test_mailgun_api_key_set():
    assert settings.MAILJET_API_KEY is not None
