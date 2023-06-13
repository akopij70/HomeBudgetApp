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

    conn.commit

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
    ids = list(c.execute(f"SELECT id FROM Incomes").fetchall())

    if id not in ids:
        raise HTTPException(
            status_code=217,
            detail="No such income in incomes (wrong id).",
        )

    income = db.get("Income", id)

    data = {}
    data["walletId"] = income[0][0]
    data["userId"] = income[0][1]
    data["amount"] = income[0][2]
    data["date"] = income[0][3]
    data["category"] = income[0][4]
    data["name"] = income[0][5]

    return data
