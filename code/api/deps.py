from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from importlib_metadata import DeprecatedTuple
from pydantic import ValidationError
from sqlalchemy.orm import Session
import crud, models, schemas

# from code.core import security
# from app.core.config import settings
from db.session import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
