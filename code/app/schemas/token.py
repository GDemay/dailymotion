""" This is the schemas for the tokens. """
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """This is the model for a token."""

    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """This is the model for a token payload."""

    sub: Optional[int] = None


class TokenBase(BaseModel):
    """This is the base model for a token."""

    id_user: int
    expires_in: int
    email_code: str


# Properties to receive via API on creation
class TokenCreate(TokenBase):
    """This is the model for creating a token."""

    id_user: int
    expires_in: datetime
    email_code: str


# Properties to receive via API on update
class TokenUpdate(TokenBase):
    """This is the model for updating a token."""

    id_user: int
    expires_in: datetime
    email_code: str


class TokenEmail(BaseModel):
    """This is the model for a token email."""

    from_email: str
    to: str
    subject: str
    text: str
