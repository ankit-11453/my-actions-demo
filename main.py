from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    age: int
    email: Optional[str] = None

class User(UserCreate):
    id: int

users_db = []

@app.get("/")
def read_root():
    return {"message": "FastAPI is running"}

@app.get("/users")
def get_users():
    return {"users": users_db}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    new_id = len(users_db) + 1
    new_user = {
        "id": new_id,
        "name": user.name,
        "age": user.age,
        "email": user.email
    }
    users_db.append(new_user)
    return new_user

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserCreate):
    for existing_user in users_db:
        if existing_user["id"] == user_id:
            existing_user["name"] = user.name
            existing_user["age"] = user.age
            existing_user["email"] = user.email
            return existing_user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for index, user in enumerate(users_db):
        if user["id"] == user_id:
            deleted_user = users_db.pop(index)
            return {"message": "User deleted", "user": deleted_user}
    raise HTTPException(status_code=404, detail="User not found")