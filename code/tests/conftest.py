import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.core.config import settings
from app.db.session import Base
from app.main import app

API_VERSION = settings.API_VERSION
# Create the new database session
user_name = "user"
password = "password"
host = "db"
database_name = "sample_db"

SQLALCHEMY_DATABASE_URL = (
    f"mysql://{user_name}:{password}@{host}/{database_name}?charset=utf8"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a new database_name name


@pytest.fixture()
def session():

    # Create the database
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):

    # Dependency override

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
