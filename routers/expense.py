from fastapi import APIRouter, HTTPException
import sqlite3


router = APIRouter(
    prefix="/Expenses",
    tags=["Expenses"],
)
e404 = HTTPException(status_code=404, detail="Data not found")

conn = sqlite3.connect("home_budget.db")
c = conn.cursor()


@router.post("/", tags=["Expense"])
async def post_expense(
    userId: int,
    walletId: int,
    amount: float,
    date: str,
    category: str,
    name: str | None = None,
):
    wallet_ownership = c.execute(
        f"SELECT * FROM 'WalletOwnership' WHERE userId = '{userId}' AND walletId = '{walletId}'"
    ).fetchall()
    if wallet_ownership:
        c.execute(
            f"INSERT INTO Expense (walletId, userId, amount, date, category, name) VALUES ('{walletId}', '{userId}', '{amount}', '{date}', '{category}','{name}',)"
        )
    else:
        return "User cant add expense to this wallet"

    return {
        "userId": userId,
        "walletId": walletId,
        "amount": amount,
        "date": date,
        "date": category,
        "name": name,
    }
