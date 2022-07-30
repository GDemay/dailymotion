from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from core.security import get_password_hash, verify_password
from crud.base import CRUDBase
from models.token import Token
from schemas.token import TokenCreate, TokenUpdate
import logging


class CRUDToken(CRUDBase[Token, TokenCreate, TokenUpdate]):
    def get_by_id(self, db: Session, *, id: int) -> Optional[Token]:
        return db.query(Token).filter(Token.id == id).first()

    def get_token_by_user_id(self, db: Session, *, id_user: int) -> Optional[Token]:
        return db.query(Token).filter(Token.id_user == id_user).first()

    def create(self, db: Session, *, obj_in: TokenCreate) -> Token:
        logging.debug("CRUDToken.create: obj_in: %s", obj_in)
        db_obj = Token(
            id_user=obj_in.id_user,
            expires_in=obj_in.expires_in,
            token_code=obj_in.token_code,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Token, obj_in: Union[TokenUpdate, Dict[str, Any]]
    ) -> Token:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def delete(self, db: Session, *, id_token: int) -> Optional[Token]:
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
