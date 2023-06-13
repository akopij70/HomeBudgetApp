from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter(
    prefix="/WishlistItems",
    tags=["WishlistItem"],
)
e404 = HTTPException(status_code=404, detail="Data not found")

conn = sqlite3.connect("home_budget.db")
c = conn.cursor()


@router.get("/{userId}")
async def get_WishlistItems(userId: int):
    try:
        WishlistItems = c.execute(
            f"SELECT * FROM WishListItem WHERE userId = {userId} "
        ).fetchall()
        print(WishlistItems)
        response = []
        for WishlistItem in WishlistItems:
            data = {}
            data["id"] = WishlistItem[0]
            data["userId"] = WishlistItem[1]
            data["name"] = WishlistItem[2]
            data["price"] = WishlistItem[3]
            response.append(data)
    except:
        raise e404

    return response


@router.get("/single/{userId}&{wishlistItemId}")
async def get_WishlistItem(userId: int, wishlistItemId: int):
    try:
        WishlistItem = c.execute(
            f"SELECT * FROM WishlistItem WHERE id = {wishlistItemId} AND userId = {userId}"
        ).fetchall()

        data = {}
        data["id"] = WishlistItem[0][0]
        data["userId"] = WishlistItem[0][1]
        data["name"] = WishlistItem[0][2]
        data["price"] = WishlistItem[0][3]
    except:
        raise e404

    return data


@router.post("/", status_code=201)
async def post_WishlistItem(userId: int, name: str, price: str):
    c.execute(
        f"INSERT INTO WishlistItem (userId, name, price) VALUES ('{userId}','{name}','{price}')"
    )
    conn.commit()
    return {"userId": userId, "name": name, "price": price}


@router.put("/{id}&{userId}&{name}")
async def put_WishlistItem(
    id: int,
    userId: int,
    name: str,
    newName: str | None = None,
    price: str | None = None,
):
    if newName:
        db.set("WishlistItem", "name", name, newName)
    if price:
        db.set("WishlistItem", "price", name, price)

    return {
        "id": id,
        "userId": userId,
        "name": newName | name,
        "price": price,
    }


@router.delete("/{name}", status_code=204)
async def delete_WishlistItem(name: str):
    db.delete("WishlistItem", name)
    return
