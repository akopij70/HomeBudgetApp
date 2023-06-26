import time
from typing import Dict
import os
import jwt
from decouple import config
from fastapi import HTTPException
import sqlite3

import dotenv

conn = sqlite3.connect("home_budget.db")
c = conn.cursor()

dotenv.load_dotenv()

# ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
# REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
JWT_ALGORITHM = "HS256"
JWT_SECRET = os.environ.get("JWT_SECRET_KEY")  # should be kept secret
# JWT_REFRESH_SECRET_KEY = os.environ["JWT_REFRESH_SECRET_KEY"]  # should be kept secret


def token_response(token: str):
    return {"access_token": token}


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {"user_id": user_id, "expires": time.time() + 600 * 3}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}


def checkChild(userId_param: int, userId_token: int):
    userType = c.execute(
        f"SELECT userType FROM USER WHERE id={userId_token}"
    ).fetchall()

    if userType[0][0].lower() == "child":
        if userId_param != userId_token:
            raise HTTPException(status_code=403, detail="What are you looking for?")
