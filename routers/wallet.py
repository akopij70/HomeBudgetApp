from fastapi import APIRouter, HTTPException
from dbmanagement.manage_db import *

db = Db("home_budget", True)
router = APIRouter()
e404 = HTTPException(status_code=404, detail="Data not found")


@router.get("/Wallets/", tags=["Wallet"])
async def get_wallets():
    try:
        wallets = db.get("Wallet", None)

        response = []
        for wallet in wallets:
            data = {}
            data["id"] = wallet[0]
            data["balance"] = wallet[1]
            data["type"] = wallet[2]
            data["name"] = wallet[3]
            response.append(data)
    except:
        raise e404

    return response


@router.get("/Wallets/{id}", tags=["Wallet"])
async def get_wallet(id: int):
    try:
        wallet = db.get("Wallet", id)

        data = {}
        data["id"] = wallet[0][0]
        data["balance"] = wallet[0][1]
        data["type"] = wallet[0][2]
        data["name"] = wallet[0][3]
    except:
        raise e404

    return data


@router.post("/Wallets/", tags=["Wallet"], status_code=201)
async def post_wallet(balance: float, type: str, name: str):
    db.insert("Wallet", [balance, type, name])
    return {"balance": balance, "type": type, "name": name}


@router.put("/Wallets/{id}", tags=["Wallet"])
async def put_wallet(
    id: int,
    balance: float | None = None,
    type: str | None = None,
    name: str | None = None,
):
    if balance:
        db.set("Wallet", "balance", id, balance)
    if type:
        db.set("Wallet", "type", id, type)
    if name:
        db.set("Wallet", "name", id, name)

    return {"id": id, "balance": balance, "type": type, "name": name}


@router.delete("/Wallets/{id}", tags=["Wallet"], status_code=204)
async def delete_wallet(id: int):
    db.delete("Wallet", str(id))
    return
