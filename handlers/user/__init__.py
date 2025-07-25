from aiogram import Router

from handlers.user.take_ref_balance import router as take_router
from handlers.user.course import router as course_router
from handlers.user.profile import router as profie_router
from handlers.user.payment import router as payment_router
from handlers.user.start import router as start_router
from handlers.user.support import router as support_router

router = Router()


router.include_routers(
    start_router, # Старт
    payment_router, # Система оплаты
    course_router, # Курсы
    profie_router, # Профиль
    support_router, # Поддержка
    take_router, # Снятие денег

)