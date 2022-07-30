import app.main as main
import pytest
from starlette.testclient import TestClient

client = TestClient(main.app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_sample():

    assert True


def test_sample2():
    assert True
