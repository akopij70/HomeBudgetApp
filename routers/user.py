from fastapi import APIRouter, HTTPException
import sqlite3

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

    return


@router.post("/login/{name}&{password}", status_code=200)
async def login_user(name: str, password: str):
    user = c.execute(f"SELECT * FROM 'User' WHERE name = '{name}'").fetchall()

    if user:
        if user[0][2] == password:
            return {"token": "123456789"}
        else:
            raise HTTPException(status_code=410, detail="Wrong password")

    else:
        raise HTTPException(status_code=410, detail="User doesnt exist")
