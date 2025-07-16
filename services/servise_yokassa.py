from yookassa import Configuration, Payment
from uuid import uuid4
from config import YOOKASSA_SHOP_ID, YOOKASSA_SECRET_KEY, BASE_URL

Configuration.account_id = YOOKASSA_SHOP_ID
Configuration.secret_key = YOOKASSA_SECRET_KEY


async def create_payment(amount: int, user_id: int, tariff_code: str):
    payment = Payment.create({
        "amount": {
            "value": f"{amount}.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f'{BASE_URL}'  # f"https://t.me/your_bot"  # после оплаты вернёт сюда
        },
        "capture": True,
        "description": f"Оплата тарифа {tariff_code} для пользователя {user_id}",
        "metadata": {
            "user_id": str(user_id),
            "tariff_code": tariff_code
        }
    }, uuid4())

    return payment.confirmation.confirmation_url, payment.id