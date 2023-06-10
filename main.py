from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse

import manage_db

db = manage_db.Db("home_budget", True)
app = FastAPI(
    title="Home Budget API", swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

e404 = HTTPException(status_code=404, detail="Data not found")


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.get("/Wallets/", tags=["Wallet"])
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


@app.get("/Wallets/{id}", tags=["Wallet"])
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


@app.post("/Wallets/", tags=["Wallet"], status_code=201)
async def post_wallet(balance: float, type: str, name: str):
    db.insert("Wallet", [balance, type, name])
    return {"balance": balance, "type": type, "name": name}


@app.put("/Wallets/{id}", tags=["Wallet"])
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


@app.delete("/Wallets/{id}", tags=["Wallet"], status_code=204)
async def delete_wallet(id: int):
    db.delete("Wallet", str(id))
    return
