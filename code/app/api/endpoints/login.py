import logging
import random
from datetime import datetime, timedelta
from typing import Any

# import app.crud, app.models, app.schemas
import app.crud as crud
import app.models.user as models
import app.schemas as schemas
from app.api import deps
from app.core.config import settings
from app.core.email import Email
from app.core.security import create_access_token
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/auth", response_model=schemas.Token)
def auth(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """OAuth2 compatible token login, get an access token for future requests


    Args:
        db (Session, optional): _description_. Defaults to Depends(deps.get_db).
        form_data (OAuth2PasswordRequestForm, optional): _description_. Defaults to Depends().

    Raises:
        HTTPException: _description_

    Returns:
        Any: _description_
    """

    logging.info("Authenticating user")

    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        logging.info("No user found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized. Incorrect email or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    logging.info("Sucessfully authenticated user")

    # TODO Create a schema
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/me", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """_summary_

    Args:
        current_user (models.User, optional): _description_. Defaults to Depends(deps.get_current_user).

    Returns:
        Any: _description_
    """
    return current_user


@router.post("/email-validator")
def email_validator(
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """This is for checking if an email is valid or not

    Args:
        current_user (models.User, optional): The user
        db (Session, optional): _description_. The db

    Raises:
        HTTPException:  If the user is not found.

    Returns:
        Any: The user.
    """

    # Check if user is active
    logging.info("Checking if user is active")
    if crud.user.is_active(current_user):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="The user is already active."
        )

    # Generate 4 digit random number
    logging.info("Generating random digits")
    random_digits = random.randint(1000, 9999)
    # This random digits has a time limit of 5 minutes

    # Look if a token already exists for this user
    token = crud.token.get_token_by_user_id(db, id_user=current_user.id)
    if token:
        logging.info("A token already exists")

        # If a token already exists, check if it is still valid
        if datetime.now() < token.expires_in:
            logging.info("Token already exists and is still valid")
            # If the token is still valid, return the token
            return token
        else:
            # If the token is expired, delete it and create a new one
            logging.debug("Token already exists but is expired")
            crud.token.delete(db, id_token=token.id)

    # create a new one
    logging.debug("Token does not exist, create a new one")

    # Send the token to the user
    return crud.token.create(
        db=db,
        obj_in=schemas.TokenCreate(
            id_user=current_user.id,
            expires_in=datetime.now()
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTE_CODE_VALIDATION),
            email_code=random_digits,
        ),
    )


# Send an email with the code to the user
@router.post("/email-validator/send")
def email_validator_send(
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """This is for sending an email with the code to the user

    Args:
        current_user (models.User, optional): The user
        db (Session, optional): _description_. The db

    Raises:
        HTTPException:  If the user is not found.

    Returns:
        Any: The user.
    """

    # call email_validator to get the token
    token = email_validator(current_user=current_user, db=db)
    # send the email with the token
    email = Email(
        to=current_user.email,
        text=f"Your email validation code is {token.email_code}",
    )

    return email.send()


@router.post("/activate-user")
def token_validator(
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
    token: str = "",
) -> Any:
    """This is for checking if an email is valid or not

    Args:
        current_user (models.User, optional): The user
        db (Session, optional): _description_. The db
        token (str, optional): _description_.  The token to validate


    Returns:
        Any: The user.
    """

    # Check if the user is active
    if crud.user.is_active(current_user):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="The user is already active."
        )
    # Get the token from the database
    Token = crud.token.get_token_by_user_id(db, id_user=current_user.id)

    # Check if a token is link to the user
    if not Token:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This token does not exists for to this user.",
        )
    # Check if the token is correct
    if Token.email_code != token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token. Please check the token and try again.",
        )

    # Check if the user is the same as the one who created the token
    if Token.id_user != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )
    # Check if the token is still valid
    if Token.expires_in < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    # Check if the user is active

    # Delete the token
    crud.token.delete(db, id_token=Token.id)

    # Set the user as active
    crud.user.set_active(db, user=current_user, is_active=True)
    # Return the user
    logging.info("User activated")
    return Token
