from sqlite3 import Date
from xmlrpc.client import DateTime

from app.db.base_class import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship


class Token(Base):
    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, nullable=True)
    expires_in = Column(DateTime, nullable=True)
    email_code = Column(String, nullable=True)
