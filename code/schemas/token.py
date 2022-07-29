from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None


class TokenBase(BaseModel):
    id_user: int
    expires_in: int
    token_code: str


# Properties to receive via API on creation
class TokenCreate(TokenBase):
    id_user: int
    expires_in: datetime
    token_code: str


# Properties to receive via API on update
class TokenUpdate(TokenBase):
    id_user: int
    expires_in: datetime
    token_code: str
