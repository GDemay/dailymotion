import random

import pytest
from starlette.testclient import TestClient

import app.main as main
from app.core.config import settings
from app.core.email import Email

client = TestClient(main.app)


def authenticate_user(email: str, password: str) -> str:
    client.headers["content-type"] = "application/x-www-form-urlencoded"
    login_data = {
        "username": email,
        "password": password,
    }
    return client.post(f"{settings.API_VERSION}/login/auth", data=login_data)


def generate_random_email():
    return (
        "".join([random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(10)])
        + "@example.com"
    )


def create_user(email: str):
    return client.post(
        f"{settings.API_VERSION}/user",
        json={
            "email": RANDOM_EMAIL,
            "is_active": False,
            "password": "test",
        },
    )


RANDOM_EMAIL = generate_random_email()
USER_ID = 0
