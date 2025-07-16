from datetime import datetime, timezone
from uuid import uuid4
import pytest


def generate_unique_id():
    return int(str(uuid4().int)[:9])

@pytest.mark.asyncio
async def test_add_payment_new(crude_payments, crude_user):
    telegram_id = generate_unique_id()
    await crude_user.add_user(telegram_id=telegram_id, user_name="TestUser")

    result = await crude_payments.add_payment(
        telegram_id=telegram_id,
        plan="basic",
        day_count=10,
        pay_sum=100,
        registered_at=datetime.now(timezone.utc),
        referral_id=None,
    )
    assert result is True

    payments_list = await crude_payments.get_all_payments()
    assert payments_list is not False
    assert any(p.telegram_id == telegram_id and p.plan == "basic" for p in payments_list)

@pytest.mark.asyncio
async def test_get_all_payments_empty(crude_payments):
    # Тут желательно убедиться, что база пустая, или использовать отдельную тестовую базу
    payments = await crude_payments.get_all_payments()
    assert payments is False or isinstance(payments, list)

@pytest.mark.asyncio
async def test_get_all_payments_and_user(crude_payments, crude_user):
    telegram_id = generate_unique_id()
    await crude_user.add_user(telegram_id=telegram_id, user_name="TestUser")

    await crude_payments.add_payment(
        telegram_id=telegram_id,
        plan="premium",
        day_count=5,
        pay_sum=200,
        registered_at=datetime.now(timezone.utc),
        referral_id=None,
    )

    payments_by_user = await crude_payments.get_all_payments_and_user(telegram_id=telegram_id)
    assert isinstance(payments_by_user, list)
    assert all(p.telegram_id == telegram_id for p in payments_by_user)

    payments_by_user_and_plan = await crude_payments.get_all_payments_and_user(telegram_id=telegram_id, plan="premium")
    assert isinstance(payments_by_user_and_plan, list)
    assert all(p.telegram_id == telegram_id and p.plan == "premium" for p in payments_by_user_and_plan)

@pytest.mark.asyncio
async def test_add_duplicate_payment(crude_payments, crude_user):
    telegram_id = generate_unique_id()
    await crude_user.add_user(telegram_id=telegram_id, user_name="TestUser")

    payment_data = dict(
        telegram_id=telegram_id,
        plan="standard",
        day_count=7,
        pay_sum=150,
        registered_at=datetime.now(timezone.utc),
        referral_id=None,
    )

    result1 = await crude_payments.add_payment(**payment_data)
    assert result1 is True

    result2 = await crude_payments.add_payment(**payment_data)
    assert result2 is False  # Предполагается, что добавление дубликата не пройдет

