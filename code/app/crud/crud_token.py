""" This is the CRUD for the tokens. """
import logging
from typing import Any, Dict, Optional, Union

from app.crud.base import CRUDBase
from app.models.token import Token
from app.schemas.token import TokenCreate, TokenUpdate
from sqlalchemy.orm import Session


class CRUDToken(CRUDBase[Token, TokenCreate, TokenUpdate]):
  """This is the CRUD class for the Token model.

  Args:
      CRUDBase (_type_): The CRUD base class that is used for the CRUD.
      Token (_type_): The model class that is used for the CRUD.
      TokenCreate (_type_): The schema class that is used for the create.
      TokenUpdate (_type_): The schema class that is used for the update.
  """
  def get_by_id(self, db: Session, *, id: int) -> Optional[Token]:
    """This is for getting a token by id."

    Args:
        db (Session): The database session.
        id (int): The id of the token.

    Returns:
        Optional[Token]: The token.
    """
    return db.query(Token).filter(Token.id == id).first()

  def get_token_by_user_id(self, db: Session, *, id_user: int) -> Optional[Token]:
    """This is for getting a token by user id."

    Args:
        db (Session): The database session.
        id_user (int): The id of the user.

    Returns:
        Optional[Token]:  The token.
    """
    return db.query(Token).filter(Token.id_user == id_user).first()

  def create(self, db: Session, *, obj_in: TokenCreate) -> Token:
    """This is for creating a token."

    Args:
        db (Session): The database session.
        obj_in (TokenCreate): The token to create.

    Returns:
        Token: The created token.
    """
    logging.debug("CRUDToken.create: obj_in: %s", obj_in)
    db_obj = Token(
        id_user=obj_in.id_user,
        expires_in=obj_in.expires_in,
        email_code=obj_in.email_code,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def update(
      self, db: Session, *, db_obj: Token, obj_in: Union[TokenUpdate, Dict[str, Any]]
  ) -> Token:
    """This is for updating a token."

    Args:
        db (Session): The database session.
        db_obj (Token): The token to update.
        obj_in (Union[TokenUpdate, Dict[str, Any]]): The token to update.

    Returns:
        Token: The updated token.
    """
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    return super().update(db, db_obj=db_obj, obj_in=update_data)

  def delete(self, db: Session, *, id_token: int) -> Optional[Token]:
    """This is for deleting a token."

    Args:
        db (Session): The database session.
        id_token (int): The id of the token to delete.

    Returns:
        Optional[Token]: The deleted token.
    """
      # Get the user_id from the token.id
    db_obj = db.query(Token).filter(Token.id == id_token).first()
    if not db_obj:
        return None

    id_user = db_obj.id_user
    # Get all the tokens of the user
    tokens = db.query(Token).filter(Token.id_user == id_user).all()

    # Delete all the tokens
    for token in tokens:
        db.delete(token)
    db.commit()
    return db_obj


token = CRUDToken(Token)
