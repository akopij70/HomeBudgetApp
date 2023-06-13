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


@router.get("/item/{userId}&{wishlistItemId}")
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
async def post_WishlistItem(userId: int, name: str, price: float):
    c.execute(
        f"INSERT INTO WishlistItem (userId, name, price) VALUES ('{userId}','{name}','{price}')"
    )
    conn.commit()
    return {"userId": userId, "name": name, "price": price}


@router.put("/{id}&{userId}&{name}")
async def put_WishlistItem(
    id: int,
    userId: int,
    newName: str | None = None,
    price: float | None = None,
):
    owner = list(c.execute(f"SELECT userId FROM WishlistItem WHERE id = {id}"))
    if owner:
        if owner[0][0] != userId:
            raise HTTPException(status_code=410, detail="Not permitted")

        if newName:
            c.execute(f"UPDATE WishlistItem SET name='{newName}' WHERE id = {id}")
        if price:
            c.execute(f"UPDATE WishlistItem SET price='{price}' WHERE id = {id}")
        conn.commit()

        return {
            "id": id,
            "userId": userId,
            "name": newName,
            "price": price,
        }
    else:
        raise HTTPException(
            status_code=410,
            detail="User/item doesnt exist or item doesnt belong to user",
        )


@router.delete("/{id}&{userId}", status_code=204)
async def delete_WishlistItem(id: int, userId: int):
    owner = list(c.execute(f"SELECT userId FROM WishlistItem WHERE id = {id}"))
    if owner:
        if owner[0][0] != userId:
            raise HTTPException(status_code=410, detail="Not permitted")

        c.execute(f"DELETE FROM WishlistItem WHERE id={id}")
        conn.commit()

        return
    else:
        raise HTTPException(
            status_code=410,
            detail="User/item doesnt exist or item doesnt belong to user",
        )
