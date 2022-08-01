import databases
import psycopg2


POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_SERVER = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DB = "sample_db"


async def create_db():
    # DATABASE = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}"

    database = Database(
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    await database.connect()

    # Create a user table
    await database.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        );
        """
    )

    # Insert a user with the username 'test' and email 'toto@gmail.com' and password 'test'
    await database.execute(
        """
        INSERT INTO users (username, email, password)
        VALUES ('test', 'bite', 'test');
        """
    )
    # GET all user from sample_db
    query = "SELECT * FROM users"
    rows = await database.fetch_all(query=query)
    # print all user
    print("High Scores:", rows)

    # Connect to the database sample_db

    await database.disconnect()


# asyncio.run(create_db())


db = psycopg2.connect(
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_SERVER,
    port=POSTGRES_PORT,
)
cursor = db.cursor()
query = """select * from users"""
cursor.execute(query)
rows = cursor.fetchall()

# Now 'rows' has all data
for x in rows:
    print(x[0], x[1])

# insert a new user name 'test2' and email 'bite' and password 'test2'
query = """INSERT INTO users (username, email, password) VALUES ('awawawa', 'wwwafd', 'test2dadda')"""
cursor.execute(query)
db.commit()

# get all users
query = """select * from users"""
cursor.execute(query)
rows = cursor.fetchall()

# Now 'rows' has all data
print(rows)
for x in rows:
    print(x)
# DROP 

db.close()
