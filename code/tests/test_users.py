import app.main as main
import app.core.config as config
import pytest
import random
from starlette.testclient import TestClient

client = TestClient(main.app)

RANDOM_STRING = (
    "".join([random.choice("abcdefghijklmnopqrstuvwxyz") for i in range(10)])
    + "@example.com"
)
USER_ID = 1


def test_get_all_users():
    response = client.get("/api/v1/user")
    assert response.status_code == 200
    return response.json()


# Create a user
def test_create_user():
    # Create a user
    response = client.post(
        "/api/v1/user",
        json={
            "email": RANDOM_STRING,
            "is_active": False,
            "full_name": "test",
            "password": "test",
        },
    )
    assert response.status_code == 200

    # Get the user
    # Get user_id
    USER_ID = response.json()["id"]
    response = client.get(f"/api/v1/user/{USER_ID}")
    assert response.status_code == 200


# Create a user with an invalid email
def test_create_user_invalid_email():
    # Create a user
    response = client.post(
        "/api/v1/user",
        json={
            "email": "invalid_email",
            "is_active": False,
            "full_name": "test",
            "password": "test",
        },
    )
    assert response.status_code == 422


# Get a wrong user with an invalid id
def test_get_user_invalid_id():
    response = client.get("/api/v1/user/0")
    assert response.status_code == 404


# Search the email of the user
def test_email_in_database():
    response = client.get(f"/api/v1/user/email/{RANDOM_STRING}")
    assert response.status_code == 200


# Search a wrong email
def test_email_not_in_database():
    fake_email = "this_is_a_bad_email@example.com"
    response = client.get(f"/api/v1/user/email/{fake_email}")
    assert response.status_code == 404


# Test if the user is active
def test_get_user_active():
    # Create a user
    response = client.get(f"/api/v1/user/{USER_ID}")
    assert response.status_code == 200
    assert response.json()["is_active"] == False
