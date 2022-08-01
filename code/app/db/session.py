""" This is the session for configuring the database."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import psycopg2
import sys
user_name = "user"
password = "password"
host = "db"
database_name = "sample_db"

DATABASE = f"mysql://{user_name}:{password}@{host}/{database_name}?charset=utf8"


ENGINE = create_engine(DATABASE, pool_pre_ping=True)
# SessionLocal = Session()
SessionLocal = sessionmaker(bind=ENGINE)

# scoped_session = scoped_session(Session)



POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_SERVER = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DB = "sample_db"

class Database:
    def __init__(self):
        self.conn = self.connect()

    def connect(self):
        """
        Connect to database and return connection
        """
        print("Connecting to PostgreSQL Database...")
        try:
            conn = psycopg2.connect(
                host=POSTGRES_SERVER,
                dbname=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                port=POSTGRES_PORT,
            )
        except psycopg2.OperationalError as e:
            print(f"Could not connect to Database: {e}")
            sys.exit(1)

        return conn