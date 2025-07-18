from aiogram import Router

from .take_ref_balance import router as take_router
from .course import router as course_router
from .profile import router as profie_router
from .payment import router as payment_router
from .start import router as start_router
from .admin_tg_groups import router as admin_tg_router
from .support import router as support_router

router = Router()


router.include_routers(
    start_router, # Старт
    payment_router, # Система оплаты
    course_router, # Курсы
    profie_router, # Профиль
    admin_tg_router, # Админ тг групп
    support_router, # Поддержка
    take_router, # Снятие денег

)

__all__ = [
    'router'
]