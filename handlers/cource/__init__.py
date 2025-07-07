from .advanced import router as advanced_router
from .all_course import router as all_course_router
from .base import router as base_router
from .exclusive import router as exclusive_router

from aiogram import Router


router = Router()


router.include_routers(
    base_router,
    advanced_router,
    exclusive_router,
    all_course_router
)

__all__ = [
    'router'
]