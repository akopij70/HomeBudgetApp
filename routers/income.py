from fastapi import APIRouter, HTTPException
from dbmanagement.manage_db import *

router = APIRouter()
e404 = HTTPException(status_code=404, detail="Data not found")


db = Db("home_budget", True)
conn = sqlite3.connect("home_budget.db")
c = conn.cursor()


@router.post("/Incomes", tags=["Income"])
async def post_income(
    walletId: int,
    userId: int,
    amount: float,
    date: str,
    category: str,
    name: str | None = None,
):
    wallets_ownerships = db.get("WalletOwnership")

    if (walletId, userId) not in wallets_ownerships:
        raise HTTPException(
            status_code=217,
            detail="Cannot add income. User/wallet does not exist or user is not the owner of the wallet.",
        )

    db.insert("Income", [walletId, userId, amount, date, category, name])

    conn.commit()

    return {
        "walletId": walletId,
        "userId": userId,
        "amount": amount,
        "date": date,
        "category": category,
        "name": name,
    }


@router.get("/Incomes", tags=["Income"])
async def get_income(id: int):
    ids = c.execute(f"SELECT id FROM Income").fetchall()
    ids = [x for tpl in ids for x in tpl]

    if id not in ids:
        raise HTTPException(
            status_code=217,
            detail="No such income in incomes (wrong id).",
        )

    income = c.execute(f"SELECT * FROM Income WHERE id = {id}").fetchall()

    data = {}
    data["walletId"] = income[0][1]
    data["userId"] = income[0][2]
    data["amount"] = income[0][3]
    data["date"] = income[0][4]
    data["category"] = income[0][5]
    data["name"] = income[0][6]

    return data


@router.put("/Incomes", tags=["Income"])
async def put_income(
    id: int,
    amount: float,
    date: str,
    name: str | None = None,
):
    ids = c.execute(f"SELECT id FROM Income").fetchall()
    ids = [x for tpl in ids for x in tpl]

    if id not in ids:
        raise HTTPException(
            status_code=217,
            detail="No such income in incomes (wrong id).",
        )

    c.execute(f"UPDATE Income SET amount = {amount} and date = \'{date}\' and  name = \'{name}\' WHERE id = {id}")
    conn.commit()

    return {
        "amount": amount,
        "date": date,
        "name": name
    }

@router.delete("/Incomes", tags=["Income"])
async def delete_income(id:int):
    ids = c.execute(f"SELECT id FROM Income").fetchall()
    ids = [x for tpl in ids for x in tpl]

    if id not in ids:
        raise HTTPException(
            status_code=217,
            detail="No such income in incomes (wrong id).",
        )

    c.execute(f"DELETE FROM Income WHERE id = {id}")
    conn.commit()

    return "Deleted successfully"
