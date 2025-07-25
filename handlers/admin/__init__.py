from aiogram import Router

from .admin_static import router as admin_static_router
# from .admin_tg_groups import router as admin_tg_groups_router

router = Router()


router.include_routers(
    admin_static_router, # Static admin commands
    # admin_tg_groups_router, # Admin TG groups management
)