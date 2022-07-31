""" This is the class for the users endpoint. """
from typing import Any, List

import app.crud as crud
import app.schemas as schemas
from app.api import deps
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """_summary_ line: This is for getting all the users

    Args:
        db (Session, optional):  Defaults to Depends(deps.get_db).
        skip (int, optional):  Defaults to 0.
        limit (int, optional): Defaults to 100.

    Returns:
      The users.
    """
    return crud.user.get_multi(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """_summary_ line: This is for getting a user by id

    Args:
        user_id (int):  The id of the user.
        db (Session, optional): Defaults to Depends(deps.get_db).

    Raises:
        HTTPException:  If the user is not found.

    Returns:
        Any: The user.
    """
    user = crud.user.get(db, id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


# Get user by email
@router.get("/email/{email}", response_model=schemas.User)
def read_user_by_email(
    email: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """_summary_ line: This is for getting a user by email

    Args:
        email (str): The email of the user.
        db (Session, optional): _description_. Defaults to Depends(deps.get_db).

    Raises:
        HTTPException:  If the user is not found.

    Returns:
        Any: The user.
    """
    user = crud.user.get_by_email(db, email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """_summary_ line: This is for creating a user

    Args:
        user_in (schemas.UserCreate): The user to create.
        db (Session, optional): The db

    Raises:
        HTTPException: If the user is not found.

    Returns:
        Any:  The user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conflict. The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


# Delete user
@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
) -> Any:
    """_summary_ line: This is for deleting a user

    Args:
        user_id (int): The id of the user.
        db (Session, optional): The db
    Returns:
        Any: The user.
    """
    user = crud.user.get(db, id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist in the system.",
        )
    crud.user.remove(db, id=user_id)
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
) -> Any:
    """_summary_ line: This is for updating a user

    Args:
        user_id (int): The id of the user.
        user_in (schemas.UserUpdate): The user to update.
        db (Session, optional): The db

    Raises:
        HTTPException: _description_

    Returns:
        Any: _description_
    """
    user = crud.user.get(db, id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist in the system.",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
