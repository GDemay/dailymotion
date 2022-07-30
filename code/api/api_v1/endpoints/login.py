from datetime import timedelta, datetime
import logging
from typing import Any
import random
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.config import settings
from core.security import get_password_hash, create_access_token

import crud, models, schemas
from api import deps


router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Check token access
    """
    return current_user


@router.post("/login/email-validator")
def email_validator(
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Create a token to active the user account
    """

    # Check if user is active
    if crud.user.is_active(current_user):
        raise HTTPException(status_code=409, detail="The user is already active.")

    # Generate 4 digit random number
    random_digits = random.randint(1000, 9999)
    # This random digits has a time limit of 5 minutes

    # Look if a token already exists for this user
    token = crud.token.get_token_by_user_id(db, id_user=current_user.id)
    if token:
        # If a token already exists, check if it is still valid
        if datetime.now() < token.expires_in:
            logging.debug("Token already exists and is still valid")
            # If the token is still valid, return the token
            return token
        else:
            # If the token is expired, delete it and create a new one
            print("Token already exists but is expired, delete it")
            logging.debug("Token already exists but is expired")
            crud.token.delete(db, id_token=token.id)

    # create a new one
    logging.debug("Token does not exist, create a new one")

    Token = crud.token.create(
        db=db,
        obj_in=schemas.TokenCreate(
            id_user=current_user.id,
            expires_in=datetime.now()
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTE_CODE_VALIDATION),
            token_code=random_digits,
        ),
    )
    # Send the token to the user
    return {
        "message": "Your token is {}".format(Token.token_code),
        "token": Token.token_code,
    }


@router.post("/login/token-validator")
def token_validator(
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
    token: str = "",
) -> Any:
    """
    Validate a token and active the user account
    """

    # Check if the user is active
    if crud.user.is_active(current_user):
        raise HTTPException(status_code=422, detail="The user is already active.")
    # Get the token from the database
    Token = crud.token.get_token_by_user_id(db, id_user=current_user.id)

    # Check if a token is link to the user
    if not Token:
        raise HTTPException(status_code=422, detail="No token found")
    # Check if the token is still valid
    if Token.expires_in < datetime.now():
        raise HTTPException(status_code=400, detail="Token expired")
    # Check if the token is correct
    if Token.token_code != token:
        raise HTTPException(status_code=400, detail="Invalid token")
    # Check if the user is the same as the one who created the token
    if Token.id_user != current_user.id:
        raise HTTPException(status_code=400, detail="Invalid token")
    # Check if the user is active

    # Delete the token
    crud.token.delete(db, id_token=Token.id)

    # Set the user as active
    crud.user.set_active(db, user=current_user, is_active=True)
    # Return the user
    print("Yes!")
    return Token
