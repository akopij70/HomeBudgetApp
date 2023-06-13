from fastapi import APIRouter, HTTPException
import sqlite3


router = APIRouter(
    prefix="/Wallets",
    tags=["Wallets"],
)
e404 = HTTPException(status_code=404, detail="Data not found")

conn = sqlite3.connect("home_budget.db")
c = conn.cursor()


@router.get("/", tags=["Wallet"])
async def get_wallets():
    wallets = c.execute(f"SELECT * FROM 'Wallet'").fetchall()
    return wallets


@router.get("/{walletId}&{userId}", tags=["Wallet"])
async def get_wallet(walletId: int, userId: int):
    wallet_ownership = c.execute(
        f"SELECT * FROM 'WalletOwnership' WHERE userId = '{userId}' AND walletId = '{walletId}'"
    ).fetchall()
    if wallet_ownership:
        data = c.execute(f"SELECT * FROM 'Wallet' WHERE id = '{walletId}'").fetchall()
    else:
        raise HTTPException(status_code=410, detail="User doesnt have this wallet")

    return data


@router.post("/{userId}&{balance}&{type}&{name}", tags=["Wallet"])
async def post_wallet(userId: int, balance: float, type: str, name: str):
    walletId = list(c.execute(f"SELECT MAX(id) FROM Wallet").fetchone())
    walletId[0] += 1
    c.execute(
        f"INSERT INTO Wallet (balance, type, name) VALUES ('{balance}', '{type}', '{name}')"
    )
    c.execute(
        f"INSERT INTO WalletOwnerShip (walletId, userId) VALUES ('{walletId}', '{userId}')"
    )
    conn.commit()
    return {"walletId": walletId[0], "userId": userId, "type": type, "name": name}


@router.put("/{userId}&{id}", tags=["Wallet"])
async def put_wallet(
    userId: int,
    id: int,
    balance: float | None = None,
    type: str | None = None,
    name: str | None = None,
):
    wallet_ownership = c.execute(
        f"SELECT * FROM 'WalletOwnership' WHERE userId = '{userId}' AND walletId = '{id}'"
    ).fetchall()

    if wallet_ownership:
        if balance:
            c.execute(f"UPDATE Wallet SET {balance}='{balance}' WHERE id = {id}")
        if type:
            c.execute(f"UPDATE Wallet SET {type}='{type}' WHERE id = {id}")
        if name:
            c.execute(f"UPDATE Wallet SET {name}='{name}' WHERE id = {id}")
    else:
        return "User doesnt have permission to this wallet"
    
    conn.commit()

    return {"id": id, "balance": balance, "type": type, "name": name}


@router.delete("/{userId}&{id}", tags=["Wallet"], status_code=204)
async def delete_wallet(userId: int, id: int):
    wallet_ownership = c.execute(
        f"SELECT * FROM 'WalletOwnership' WHERE userId = '{userId}' AND walletId = '{id}'"
    ).fetchall()

    if wallet_ownership:
        c.execute(f"DELETE FROM Wallet WHERE id = {id}")
        conn.commit()
    else:
        return "User doesnt have permission to this wallet"
