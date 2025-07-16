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
# Айди Групп
grps = raz_admins(os.getenv('GROUP_IDS'))
GROUP_IDS = {
    grps[0] : 'base',
    grps[1] : 'advanced',
    grps[2] : 'exclusive',
    grps[3] : 'all',
    'links_list': grps
}
# Токен бота
TOKEN_BOT = os.getenv('TOKEN_BOT')

# Реферальная ссылка
REFFER_LINK = (os.getenv('REFFER_LINK')
               .replace('YourBot', 'PremiumNFTVideobot')  # Меняем на имя бота свое
               )  # Удаляем конец для возможности поставки ссылку
# Пример: https://t.me/PremiumNFTVideobot?start=Нужный вам айди

# Айди Магазина
YOOKASSA_SHOP_ID = int(os.getenv('YOOKASSA_SHOP_ID')) if not None else 1
# Ключ Магазина
YOOKASSA_SECRET_KEY = os.getenv('YOOKASSA_SECRET_KEY')
# Адрес после оплаты для переадресации
BASE_URL = os.getenv('BASE_URL'),'https://t.me/remiumNFTVideobot'

