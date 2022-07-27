from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from db import Base
from db import ENGINE


class UserTable(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class User(BaseModel):
    id: int
    email: str
    hashed_password: str


def main():
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()
