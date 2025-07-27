from aiogram import Router

from .admin_static import router as admin_static_router
from .admin_tg_groups import router as admin_tg_groups_router
from .admin_pay_handler_test import router as admin_pay_handler_test_router

router = Router()


router.include_routers(
    admin_static_router, # Static admin commands
    admin_tg_groups_router, # Admin TG groups management
    admin_pay_handler_test_router, # Admin payment handler test
)