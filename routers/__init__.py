from .wallet import router as wallet_router
from .user import router as user_router
from .WishlistItem import router as WishlistItem_router
from .income import router as income_router
from .expense import router as expense_router

# Define the __all__ list to specify the exported objects
__all__ = ["wallet_router", "user_router", "WishlistItem_router", "income_router", "expense_router"]
