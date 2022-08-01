import psycopg2
import sys

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
  
    def disconnect(self):
        """
        Disconnect from database
        """
        print("Disconnecting from PostgreSQL Database...")
        self.conn.close()
        return True
    def execute(self, query, *args):
        """
        Execute a query
        """
        print(f"Executing query: {query}")
        cursor = self.conn.cursor()
        cursor.execute(query, *args)
        self.conn.commit()
        return cursor
      
    def fetch_all(self, query, *args):
        """
        Fetch all rows
        """
        cursor = self.execute(query, *args)
        return cursor.fetchall()
    def fetch_one(self, query, *args):
        """
        Fetch one row
        """
        cursor = self.execute(query, *args)
        return cursor.fetchone()
      
    def fetch_column(self, query, *args):
        """
        Fetch one column
        """
        cursor = self.execute(query, *args)
        return cursor.fetchone()[0]