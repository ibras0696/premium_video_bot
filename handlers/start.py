from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext, command: CommandStart):
    # Чистка состояний
    await state.clear()
    # Берем реферальный код в случае присутствия
