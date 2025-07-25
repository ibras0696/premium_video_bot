from aiogram import Router

from .user import router as user_router
from .admin import router as admin_router

router = Router()


router.include_routers(
    user_router,  # User-related handlers
    admin_router,  # Admin-related handlers
)

__all__ = [
    'router'
]