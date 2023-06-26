from fastapi import APIRouter, HTTPException, Depends
import sqlite3
from utils import signJWT, decodeJWT, checkChild
from bearer import JWTBearer


router = APIRouter(
    prefix="/Category",
    tags=["Category"],
)
e404 = HTTPException(status_code=404, detail="Data not found")

conn = sqlite3.connect("home_budget.db")
c = conn.cursor()


@router.get("/", dependencies=[Depends(JWTBearer())])
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


@router.get("/name/{name}", dependencies=[Depends(JWTBearer())])
async def get_category(name: str):
    try:
        category = c.execute(f"SELECT * FROM Category WHERE name = '{name}'").fetchall()

        data = {}
        data["name"] = category[0][0]
    except:
        raise e404

    return data


@router.get("/expenses/{userId}&{name}", dependencies=[Depends(JWTBearer())])
async def get_expenses_by_category(
    userId: int, name: str, token: dict = Depends(JWTBearer())
):
    checkChild(userId, decodeJWT(token)["user_id"])
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
