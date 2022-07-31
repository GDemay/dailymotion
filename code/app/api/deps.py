from typing import Generator

import app.crud as crud
import app.models.user as models
import app.schemas as schemas
from app.core.config import settings
from app.db.session import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_VERSION}/login/auth")


def get_db() -> Generator:
    """_summary_ line: This is for getting the database session.

    Yields:
        Generator: The database session.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    """_summary_ line: This is for getting the current user.

    Args:
        db (Session, optional): Defaults to Depends(get_db). The database session.
        token (str, optional): Defaults to Depends(reusable_oauth2). The token.


    Returns:
        models.User: The current user.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from e

    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
