""" This is the session for configuring the database."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

user_name = "user"
password = "password"
host = "db"
database_name = "sample_db"

DATABASE = f"mysql://{user_name}:{password}@{host}/{database_name}?charset=utf8"


ENGINE = create_engine(DATABASE, pool_pre_ping=True)
# SessionLocal = Session()
SessionLocal = sessionmaker(bind=ENGINE)

# scoped_session = scoped_session(Session)

Base = declarative_base()
