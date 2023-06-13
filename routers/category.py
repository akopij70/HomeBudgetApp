from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter(
    prefix="/Category",
    tags=["Category"],
)
e404 = HTTPException(status_code=404, detail="Data not found")

conn = sqlite3.connect("home_budget.db")
c = conn.cursor()


@router.get("/")
async def get_categories():
    try:
        categories = c.execute(f"SELECT * FROM Category").fetchall()

        response = []
        for category in categories:
            data = {}
            data["name"] = category[0]
            response.append(data)
    except:
        raise e404

    return response


@router.get("/name/{name}")
async def get_category(name: str):
    try:
        category = c.execute(f"SELECT * FROM Category WHERE name = '{name}'").fetchall()

        data = {}
        data["name"] = category[0][0]
    except:
        raise e404

    return data


@router.get("/expenses/{userId}&{name}")
async def get_expenses_by_category(userId: int, name: str):
    try:
        expenses = c.execute(f"SELECT * FROM Expense WHERE category = '{name}'")

        response = []
        for expense in expenses:
            data = {}
            data["id"] = expense[0]
            data["walletId"] = expense[1]
            data["amount"] = expense[2]
            data["date"] = expense[3]
            data["category"] = expense[4]
            data["name"] = expense[5]

            response.append(data)
    except:
        raise e404

    return data
