"""_This is the base class for all the models."""
from typing import Any, Dict, Optional, Union

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from sqlalchemy.orm import Session


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
  """This is the CRUD class for the User model.

  Args:
      CRUDBase (_type_): The CRUD base class that is used for the CRUD.
      User (_type_): The model class that is used for the CRUD.
      UserCreate (_type_): The schema class that is used for the create.
      UserUpdate (_type_): The schema class that is used for the update.
      
  """
  def get(self, db: Session, *, id: int) -> Optional[User]:
    """_summary_line: This is for getting a user by id

    Args:
        db (Session): The database session.
        id (int): The id of the user.

    Returns:
        Optional[User]: The user.
    """
    return db.query(User).filter(User.id == id).first()

  def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
    """_summary_ line: This is for getting a user by email

    Args:
        db (Session): The database session.
        email (str): The email of the user.

    Returns:
        Optional[User]: The user.
    """
    return db.query(User).filter(User.email == email).first()

  def create(self, db: Session, *, obj_in: UserCreate) -> User:
    """_summary_ line: This is for creating a user

    Args:
        db (Session): The database session.
        obj_in (UserCreate): The user to create.

    Returns:
        User: The created user.
    """
    db_obj = User(
        email=obj_in.email,
        hashed_password=get_password_hash(obj_in.password),
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def update(
      self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
  ) -> User:
    """_summary_ line: This is for updating a user

    Args:
        db (Session): The database session.
        db_obj (User): The user to update.
        obj_in (Union[UserUpdate, Dict[str, Any]]): The user to update.

    Returns:
        User: The updated user.
    """
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    if update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
    return super().update(db, db_obj=db_obj, obj_in=update_data)

  def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
    """_summary_ line: This is for authenticating a user

    Args:
        db (Session): The database session.
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        Optional[User]: The user.
    """
    user = self.get_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

  def is_active(self, user: User) -> bool:
    """_summary_ line: This is for checking if a user is active

    Args:
        user (User): The user to check.

    Returns:
        bool: If the user is active.
    """
    return user.is_active

  def set_active(self, db: Session, *, user: User, is_active: bool) -> User:
    user.is_active = is_active
    db.commit()
    return user


user = CRUDUser(User)
