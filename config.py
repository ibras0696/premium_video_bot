import os
import dotenv

dotenv.load_dotenv()


# Разбор ID админов переданный в env и преобразование
def raz_admins(s: str) -> list[int]:
    txt = s.split(',')
    st = [int(i) for i in txt]
    return st


# Айди Администратора TG
ADMIN_IDS = raz_admins(os.getenv('ADMIN_IDS'))
# Токен бота
TOKEN_BOT = os.getenv('TOKEN_BOT')

# Реферальная ссылка
REFFER_LINK = (os.getenv('REFFER_LINK')
               .replace('YourBot', 'PremiumNFTVideobot')  # Меняем на имя бота свое
               )  # Удаляем конец для возможности поставки ссылку
# Пример: https://t.me/PremiumNFTVideobot?start=Нужный вам айди

