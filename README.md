## VirtualEnv init

1. `python -m venv HomeBudgetEnv`
2.  - On Windows powershell `.\HomeBudgetEnv\Scripts\Activate.ps1`
    - On Unix `source HomeBudgetEnv/bin/activate`
3. `pip install -r requirements.txt`

---

## Server

`uvicorn main:app --reload`

---

## Project structure

-   [**main**.py](./main.py)
-   [routers](./routers)
    -   [**init**.py](./routers/__init__.py)
    -   [wallet.py](./routers/wallet.py)
    -   [user.py](./routers/user.py)
    -   [WishlistItem.py](./routers/WishlistItem.py)
-   [dbmanagement](./dbmanagement)
    -   [**init**.py](./dbmanagement/__init__.py)
    -   [manage_db.py](./dbmanagement/manage_db.py)
    -   etc

---

To develop new endpoints, add scripts similarly as in wallet.py example
