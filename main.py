from fastapi import FastAPI

from routers.wallet import router as wallet_router
from routers.user import router as user_router
from routers.wishlistitem import router as WishlistItem_router
from routers.income import router as income_router
from routers.expense import router as expense_router

app = FastAPI(
    title="Home Budget API", swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

app.include_router(wallet_router)
app.include_router(user_router)
app.include_router(WishlistItem_router)
app.include_router(income_router)
app.include_router(expense_router)