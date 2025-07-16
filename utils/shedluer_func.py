from aiogram import Bot

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from config import TOKEN_BOT
from database import CrudeSubscriptions, Subscriptions
from utils.message_texts import push_subs_text
from utils.admin_kick_func import kick_user_if_not_admin

# Экземпляр бота для работы
bot_tg = Bot(token=TOKEN_BOT)


async def users_push_and_kick_group(bot: Bot = bot_tg):
    sbu_con = CrudeSubscriptions()
    # Полуычение данных подписок
    subs = await sbu_con.all_reduce_subscriptions()
    if subs:
        for sub in subs:
            if 0 < sub.day_count < 3:
                await bot.send_message(sub.telegram_id, await push_subs_text(sub.day_count, sub.plan))
            elif sub.day_count == 0:
                try:
                    # айди групп
                    grp_id = Subscriptions.get_group_ids().get(sub.plan)
                    print('\n\n\n', grp_id, '\n\n\n')
                    if grp_id:
                        await kick_user_if_not_admin(bot, sub.telegram_id, grp_id)
                except Exception as ex:
                    print(f'Ошибка при удаление с группы: {ex}')


def setup_scheduler(hour: int = 0, minute: int = 0) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    scheduler.add_job(
        users_push_and_kick_group,  # ← без ()
        trigger=CronTrigger(hour=hour, minute=minute),
        id="reduce_subs",
        replace_existing=True,
    )

    scheduler.start()
    print("📅 Шедулер запущен (каждый день в 00:00 МСК)")
    return scheduler
