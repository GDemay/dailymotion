""" This is the session for configuring the database."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from app.core.config import settings

username = settings.MYSQL_USERNAME
password = settings.MYSQL_PASSWORD
mysql_host = settings.MYSQL_HOST
database = settings.MYSQL_DATABASE

DATABASE = f"mysql://{username}:{password}@{mysql_host}/{database}?charset=utf8"


ENGINE = create_engine(DATABASE, pool_pre_ping=True)
# SessionLocal = Session()
SessionLocal = sessionmaker(bind=ENGINE)

# scoped_session = scoped_session(Session)

Base = declarative_base()
