# from aiogram import Router, Bot
# from aiogram.types import ChatJoinRequest, Message, ChatMemberUpdated
# from aiogram.filters import Command
# from aiogram.types import ChatMemberUpdated
# from aiogram.enums import ChatMemberStatus
# from aiogram.exceptions import TelegramBadRequest
#
# from database import CrudeUser, CrudeSubscriptions, Subscriptions
# from config import GROUP_IDS, grps
#
# router = Router()
#
#
# # @router.message(Command('del'))
# # async def del_test_router(message: Message):
# #     await CrudeSubscriptions().all_reduce_subscriptions(29)
# #     await message.answer('Уменишилось дней подписки')
# #
# #
# # @router.message(Command('one'))
# # async def del_test_router(message: Message):
# #     await CrudeSubscriptions().all_reduce_subscriptions(1)
# #     await message.answer('Уменьшилось дней подписки')
#
# # Обработка заявок на вступление
# @router.chat_join_request()
# async def handle_join_request(request: ChatJoinRequest, bot: Bot):
#     user_id = request.from_user.id
#     chat_id = request.chat.id
#
#     gr_dict = GROUP_IDS
#     plan = gr_dict.get(chat_id)
#
#     if chat_id in grps:
#         sub_user = await CrudeSubscriptions().check_subscription(telegram_id=user_id, plan=plan)
#         if sub_user and sub_user.day_count > 0:
#             await bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)
#             return
#
#     # ❌ Отклоняем без блокировки (не баним!)
#     await bot.decline_chat_join_request(chat_id=chat_id, user_id=user_id)
#
#
# @router.chat_member()
# async def kick_on_join_if_no_sub(event: ChatMemberUpdated):
#     # Проверяем, стал ли участником
#     if event.old_chat_member.status in (ChatMemberStatus.LEFT, ChatMemberStatus.KICKED) and \
#        event.new_chat_member.status == ChatMemberStatus.MEMBER:
#
#         user_id = event.from_user.id
#         chat_id = event.chat.id
#
#         group_tariffs = Subscriptions.get_group_ids()
#
#         # Определяем тариф по chat_id
#         plan = None
#         for tariff, gid in group_tariffs.items():
#             if str(gid) == str(chat_id):
#                 plan = tariff
#                 break
#
#         if not plan:
#             return
#
#         try:
#             subscription = await CrudeSubscriptions().check_subscription(user_id, plan)
#
#             if not subscription or subscription.day_count <= 0:
#                 try:
#                     await event.bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
#                     await event.bot.unban_chat_member(chat_id=chat_id, user_id=user_id)
#                     print(f"❌ {user_id} кикнут при входе в {chat_id} — нет подписки на {plan}")
#                 except TelegramBadRequest as e:
#                     print(f"⚠️ Ошибка при кике: {e}")
#         except Exception as e:
#             print(f"❌ Ошибка при проверке подписки: {e}")
