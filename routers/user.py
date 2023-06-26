from fastapi import APIRouter, HTTPException
import sqlite3
from utils import signJWT

router = APIRouter(
    prefix="/users",
    tags=["User"],
)
e404 = HTTPException(status_code=404, detail="Data not found")

conn = sqlite3.connect("home_budget.db")
c = conn.cursor()


@router.post("/signup/{name}&{password}&{userType}", status_code=200)
async def signup_user(name: str, password: str, userType: str):
    # Is user already signed up
    user = c.execute(f"SELECT * FROM 'User' WHERE name = '{name}'").fetchall()

    if user:
        raise HTTPException(status_code=410, detail="User already exists")

    c.execute(
        f"INSERT INTO User (name,password,userType) VALUES ('{name}','{password}','{userType}')"
    )

    conn.commit()

    userId = list(c.execute(f"SELECT MAX(id) FROM User").fetchone())
    return signJWT(userId[0])


@router.post("/login/{name}&{password}", status_code=200)
async def login_user(name: str, password: str):
    user = c.execute(f"SELECT * FROM 'User' WHERE name = '{name}'").fetchall()

    if not user:
        raise HTTPException(status_code=410, detail="User doesnt exist")

    if check_user(name, password):
        return signJWT(user[0][0])
    else:
        raise HTTPException(status_code=410, detail="Wrong password/username")


def check_user(user_name: str, user_password: str):
    user = c.execute(
        f"SELECT name,password FROM User WHERE name = '{user_name}' AND password = '{user_password}'"
    ).fetchall()
    if user:
        return True
    return False
