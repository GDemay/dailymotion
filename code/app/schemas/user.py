""" Pydantic schema for a user. """
from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    """_summary_ : This is the base model for a user."""

    email: Optional[EmailStr] = None
    is_active: Optional[bool] = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    """_summary_ : This is the model for creating a user."""

    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    """_summary_ : This is the model for updating a user."""

    password: Optional[str] = None


class UserInDBBase(UserBase):
    """_summary_ : This is the base model for a user in the database."""

    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    """_summary_ : This is the model for a user."""

    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    """_summary_ : This is the model for a user in the database."""

    hashed_password: str
