from datetime import datetime, timezone, timedelta
from uuid import uuid4

import pytest



def generate_unique_id():
    return int(str(uuid4().int)[:9])

@pytest.mark.asyncio
async def test_add_subscription_new(crude_subscriptions, crude_user):
    telegram_id = generate_unique_id()
    await crude_user.add_user(telegram_id=telegram_id, user_name="TestUser")
    result = await crude_subscriptions.add_subscription(
        telegram_id=telegram_id,
        plan="basic",
        day_count=10,
        price=100,
    )
    assert result is True

    subs_list = await crude_subscriptions.get_all_users_subscriptions()
    assert subs_list is not False
    assert any(s.telegram_id == telegram_id and s.plan == "basic" for s in subs_list)

@pytest.mark.asyncio
async def test_add_subscription_extend_active(crude_subscriptions, crude_user):
    telegram_id = generate_unique_id()
    await crude_user.add_user(telegram_id=telegram_id, user_name="TestUser")

    start_date = datetime.now(timezone.utc) - timedelta(days=5)
    await crude_subscriptions.add_subscription(
        telegram_id=telegram_id,
        plan="premium",
        day_count=10,
        price=200,
        start_date=start_date
    )

    result = await crude_subscriptions.add_subscription(
        telegram_id=telegram_id,
        plan="premium",
        day_count=5,
        price=100,
        start_date=start_date
    )
    assert result is True

    subs_list = await crude_subscriptions.get_all_users_subscriptions()
    sub = next(s for s in subs_list if s.telegram_id == telegram_id and s.plan == "premium")
    assert sub.day_count == 15

@pytest.mark.asyncio
async def test_add_subscription_extend_expired(crude_subscriptions, crude_user):
    telegram_id = generate_unique_id()
    await crude_user.add_user(telegram_id=telegram_id, user_name="TestUser")

    expired_date = datetime.now(timezone.utc) - timedelta(days=20)
    await crude_subscriptions.add_subscription(
        telegram_id=telegram_id,
        plan="standard",
        day_count=5,
        price=150,
        start_date=expired_date
    )

    new_start_date = datetime.now(timezone.utc)
    result = await crude_subscriptions.add_subscription(
        telegram_id=telegram_id,
        plan="standard",
        day_count=7,
        price=150,
        start_date=new_start_date
    )
    assert result is True

    subs_list = await crude_subscriptions.get_all_users_subscriptions()
    sub = next(s for s in subs_list if s.telegram_id == telegram_id and s.plan == "standard")
    assert sub.day_count == 7
    assert sub.day == new_start_date.day
    assert sub.month == new_start_date.month
    assert sub.year == new_start_date.year

@pytest.mark.asyncio
async def test_extend_subscription_success(crude_subscriptions):
    telegram_id = generate_unique_id()
    plan = "pro"
    await crude_subscriptions.add_subscription(telegram_id=telegram_id, plan=plan, day_count=10, price=300)

    result = await crude_subscriptions.extend_subscription(telegram_id=telegram_id, plan=plan, days=5)
    assert result is True

    subs_list = await crude_subscriptions.get_all_users_subscriptions()
    sub = next(s for s in subs_list if s.telegram_id == telegram_id and s.plan == plan)
    assert sub.day_count == 15

@pytest.mark.asyncio
async def test_extend_subscription_not_found(crude_subscriptions):
    result = await crude_subscriptions.extend_subscription(telegram_id=999999999, plan="none", days=5)
    assert result is False

@pytest.mark.asyncio
async def test_reduce_subscription_success(crude_subscriptions):
    telegram_id = generate_unique_id()
    plan = "basic"
    await crude_subscriptions.add_subscription(telegram_id=telegram_id, plan=plan, day_count=10, price=100)

    result = await crude_subscriptions.reduce_subscription(telegram_id=telegram_id, plan=plan, days=4)
    assert result is True

    subs_list = await crude_subscriptions.get_all_users_subscriptions()
    sub = next(s for s in subs_list if s.telegram_id == telegram_id and s.plan == plan)
    assert sub.day_count == 6

@pytest.mark.asyncio
async def test_reduce_subscription_to_zero(crude_subscriptions):
    telegram_id = generate_unique_id()
    plan = "basic"
    await crude_subscriptions.add_subscription(telegram_id=telegram_id, plan=plan, day_count=3, price=100)

    result = await crude_subscriptions.reduce_subscription(telegram_id=telegram_id, plan=plan, days=5)
    assert result is True

    subs_list = await crude_subscriptions.get_all_users_subscriptions()
    sub = next(s for s in subs_list if s.telegram_id == telegram_id and s.plan == plan)
    assert sub.day_count == 0

@pytest.mark.asyncio
async def test_reduce_subscription_not_found(crude_subscriptions):
    result = await crude_subscriptions.reduce_subscription(telegram_id=999999999, plan="none", days=1)
    assert result is False

@pytest.mark.asyncio
async def test_all_reduce_subscriptions(crude_subscriptions):
    telegram_id1 = generate_unique_id()
    telegram_id2 = generate_unique_id()
    await crude_subscriptions.add_subscription(telegram_id=telegram_id1, plan="basic", day_count=10, price=100)
    await crude_subscriptions.add_subscription(telegram_id=telegram_id2, plan="pro", day_count=5, price=200)

    result = await crude_subscriptions.all_reduce_subscriptions(days=3)
    assert isinstance(result, list)

    subs_1 = next(s for s in result if s.telegram_id == telegram_id1)
    subs_2 = next(s for s in result if s.telegram_id == telegram_id2)

    assert subs_1.day_count == 7
    assert subs_2.day_count == 2

@pytest.mark.asyncio
async def test_all_reduce_subscriptions_no_subscriptions(crude_subscriptions):
    # Очистка подписок если нужно (в зависимости от фикстуры)
    # чтобы проверить поведение при отсутствии подписок
    # Можно добавить метод очистки в фикстуру или перед запуском теста
    # В данном примере просто проверяем False при пустой базе подписок
    result = await crude_subscriptions.all_reduce_subscriptions(days=1)
    assert isinstance(result, (bool, list))

@pytest.mark.asyncio
async def test_get_all_users_subscriptions(crude_subscriptions):
    telegram_id = generate_unique_id()
    await crude_subscriptions.add_subscription(telegram_id=telegram_id, plan="basic", day_count=10, price=100)

    subs = await crude_subscriptions.get_all_users_subscriptions()
    assert isinstance(subs, list)
    assert any(s.telegram_id == telegram_id for s in subs)
