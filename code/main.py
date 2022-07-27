from typing import List

from api.api_v1.api import api_router
from db.session import SessionLocal
from fastapi import FastAPI
from model import User, UserTable
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/users")
def read_users():
    # Display all users
    users = SessionLocal.query(UserTable).all()
    return users


@app.get("/users/{user_id}")
def read_user(user_id: int):
    user = SessionLocal.query(UserTable).filter(UserTable.id == user_id).first()
    if user:
        return user
    return {"message": "User not found"}


@app.post("/user")
async def create_user(name: str, email: str, hashed_password: str):
    user = UserTable()
    user.email = email
    user.hashed_password = hashed_password
    SessionLocal.add(user)
    SessionLocal.commit()
    id = user.id
    return {"message": "User created", "user": user}


@app.put("/users")
async def update_users(users: List[User]):
    for new_user in users:
        user = SessionLocal.query(UserTable).filter(UserTable.id == new_user.id).first()
        user.email = new_user.email
        user.hashed_password = new_user.hashed_password
        SessionLocal.commit()


# Delete user by id
@app.delete("/users")
async def delete_user(user_id: int):
    # Check if the user exists
    user = SessionLocal.query(UserTable).filter(UserTable.id == user_id).first()
    # If the user exists, delete it
    if user:
        SessionLocal.delete(user)
        SessionLocal.commit()
        return {"message": "User deleted"}
    # If the user does not exist, return a 404 error
    return {"message": "User not found"}
