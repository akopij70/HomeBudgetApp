from fastapi import APIRouter, HTTPException
from dbmanagement.manage_db import *

db = Db("home_budget", True)
router = APIRouter(
    prefix="/users",
    tags=["User"],
)
e404 = HTTPException(status_code=404, detail="Data not found")


@router.get("/")
async def get_users():
    try:
        users = db.get("User", None)

        response = []
        for user in users:
            data = {}
            data["id"] = user[0]
            data["name"] = user[1]
            data["password"] = user[2]
            data["userType"] = user[3]
            response.append(data)
    except:
        raise e404

    return response


@router.get("/{name}")
async def get_user(name: str):
    try:
        user = db.get("User", name)

        data = {}
        data["id"] = user[0][0]
        data["balance"] = user[0][1]
        data["type"] = user[0][2]
        data["name"] = user[0][3]
    except:
        raise e404

    return data


@router.post("/", status_code=201)
async def post_user(name: str, password: str, userType: str):
    db.insert("User", [name, password, userType])
    return {"name": name, "password": password, "userType": userType}


@router.put("/{id}&{name}")
async def put_user(
    id: int,
    name: str,
    newName: str | None = None,
    password: str | None = None,
    userType: str | None = None,
):
    if name:
        db.set("User", "name", name, newName)
    if password:
        db.set("User", "password", name, password)
    if name:
        db.set("User", "userType", name, userType)

    return {"id": id, "name": newName, "password": password, "userType": userType}


@router.delete("/{name}", status_code=204)
async def delete_user(name: str):
    db.delete("User", name)
    return
