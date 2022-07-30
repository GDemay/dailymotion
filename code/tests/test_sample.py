import app.main as main
import pytest
from starlette.testclient import TestClient
from app.db.session import ENGINE, Base

client = TestClient(main.app)

# Will create database and tables for tests
@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=ENGINE)
    yield
    Base.metadata.drop_all(bind=ENGINE)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_sample():
    assert True


def test_sample2():
    assert True
