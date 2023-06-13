from .wallet import router as wallet_router
from .user import router as user_router
from .wishlistitem import router as WishlistItem_router
from .income import router as income_router
from .category import router as category_router


# Define the __all__ list to specify the exported objects
__all__ = [
    "wallet_router",
    "user_router",
    "WishlistItem_router",
    "income_router",
    "category_router",
]
