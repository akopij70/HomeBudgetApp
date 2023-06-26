from fastapi import APIRouter, HTTPException, Depends
import sqlite3
from dbmanagement.manage_db import *
from utils import signJWT, decodeJWT, checkChild
from bearer import JWTBearer


router = APIRouter(
    prefix="/Expenses",
    tags=["Expense"],
)
e404 = HTTPException(status_code=404, detail="Data not found")

db = Db("home_budget", True)
conn = sqlite3.connect("home_budget.db")
c = conn.cursor()


@router.post(
    "/AddExpense{userId}&{walletId}&{amount}&{date}&{category}&{name}",
    tags=["Expense"],
    dependencies=[Depends(JWTBearer())],
)
async def post_expense(
    userId: int,
    walletId: int,
    amount: float,
    date: str,
    category: str,
    name: str | None = None,
    token: dict = Depends(JWTBearer()),
):
    checkChild(userId, decodeJWT(token)["user_id"])
    wallet_ownership = c.execute(
        f"SELECT * FROM 'WalletOwnership' WHERE userId = '{userId}' AND walletId = '{walletId}'"
    ).fetchall()
    if wallet_ownership:
        db.insert("Expense", [walletId, userId, amount, date, category, name])
        conn.commit()
    else:
        raise HTTPException(
            status_code=400, detail="User cant add expense to this wallet"
        )

    return {
        "userId": userId,
        "walletId": walletId,
        "amount": amount,
        "date": date,
        "category": category,
        "name": name,
    }


@router.get(
    "/SearchExpense{userId}&{expenseId}",
    tags=["Expense"],
    dependencies=[Depends(JWTBearer())],
)
async def get_income(expenseId: int, userId: int, token: dict = Depends(JWTBearer())):
    checkChild(userId, decodeJWT(token)["user_id"])
    users_expense = c.execute(
        f"SELECT * FROM 'Expense' WHERE userId = '{userId}' AND id = '{expenseId}'"
    ).fetchall()

    if users_expense:
        return users_expense
    else:
        raise HTTPException(status_code=400, detail="Couldnt find users expense")


@router.delete(
    "/DeleteExpense{userId}&{expenseId}",
    tags=["Expense"],
    dependencies=[Depends(JWTBearer())],
)
async def delete_expense(
    userId: int, expenseId: int, token: dict = Depends(JWTBearer())
):
    checkChild(userId, decodeJWT(token)["user_id"])
    users_expense = c.execute(
        f"SELECT * FROM 'Expense' WHERE userId = '{userId}' AND id = '{expenseId}'"
    ).fetchall()

    if users_expense:
        c.execute(f"DELETE FROM Expense WHERE id = {expenseId}")
        conn.commit()
        return f"Deleted expense {users_expense}"
    else:
        raise HTTPException(status_code=400, detail="Couldnt find users expense")


@router.put(
    "/ChangeExpense/{userId}&{expenseId}",
    tags=["Expense"],
    dependencies=[Depends(JWTBearer())],
)
async def change_expense(
    userId: int,
    expenseId: int,
    amount: float | None = None,
    date: str | None = None,
    name: str | None = None,
    token: dict = Depends(JWTBearer()),
):
    checkChild(userId, decodeJWT(token)["user_id"])
    users_expense = c.execute(
        f"SELECT * FROM 'Expense' WHERE userId = '{userId}' AND id = '{expenseId}'"
    ).fetchall()

    if users_expense:
        if amount:
            c.execute(f"UPDATE Expense SET amount = {amount} WHERE id = {expenseId}")
        if date:
            c.execute(f"UPDATE Expense SET date = '{date}' WHERE id = {expenseId}")
        if name:
            c.execute(f"UPDATE Expense SET name = '{name}' WHERE id = {expenseId}")
        conn.commit()
        raise HTTPException(status_code=200, detail="Succesfully modified expense")
    else:
        raise HTTPException(status_code=400, detail="Couldnt find users expense")
