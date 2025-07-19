from yookassa import Payment, Configuration
from uuid import uuid4

from config import YOOKASSA_SECRET_KEY, YOOKASSA_SHOP_ID

# 🔐 Настройки ЮKassa
Configuration.account_id = YOOKASSA_SHOP_ID
Configuration.secret_key = YOOKASSA_SECRET_KEY


def create_payment(
    amount: float,
    telegram_id: str | int,
    return_url: str = 'https://yookassa.ru',
    description: str = 'Покупка Подписки Премиум',
    email: str = 'test@example.com'
):
    """
    Создание платежа
    :return: {'pay_url': ..., 'pay_id': ...}
    """

    payment = Payment.create({
        "amount": {
            "value": f"{amount:.2f}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": return_url
        },
        "capture": True,
        "description": description,
        "metadata": {  # ✅ Исправлено с meta_data на metadata
            "telegram_id": str(telegram_id)
        },

    }, uuid4().hex)

    return {
        'pay_url': payment.confirmation.confirmation_url,
        'pay_id': payment.id
    }


# Проверка вручную по ID
def checkout_payment(payment_id: str) -> bool | None:
    """
    Проверка статуса платежа по ID
    :return: True если оплачен, None — если в ожидании, False — отменён/истёк
    """
    payment = Payment.find_one(payment_id)

    if payment.status == 'succeeded':
        return True
    elif payment.status == 'pending':
        return None
    else:
        return False

data = create_payment(
    1,
    1,

)
print(data['pay_url'])
print(checkout_payment(data['pay_id']))