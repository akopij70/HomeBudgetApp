from fastapi import FastAPI

from routers.wallet import router as wallet_router
from routers.user import router as user_router


app = FastAPI(
    title="Home Budget API", swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

app.include_router(wallet_router)
app.include_router(user_router)
