from sqlite3 import Date
from xmlrpc.client import DateTime
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from db.base_class import Base


class Token(Base):
    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, nullable=True)
    expires_in = Column(DateTime, nullable=True)
    token_code = Column(String, nullable=True)
