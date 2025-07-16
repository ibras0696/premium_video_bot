import pytest
from uuid import uuid4


def generate_unique_id():
    """Генерирует уникальный telegram_id"""
    return int(str(uuid4().int)[:9])  # максимум 9 цифр


@pytest.mark.asyncio
async def test_add_user_new(crude_user):
    telegram_id = generate_unique_id()
    result = await crude_user.add_user(telegram_id=telegram_id, user_name="TestUser")
    assert result is False  # False = новый добавлен

    user = await crude_user.get_user(telegram_id)
    assert user is not None
    assert user.telegram_id == telegram_id
    assert user.user_name == "TestUser"


@pytest.mark.asyncio
async def test_add_user_existing(crude_user):
    telegram_id = generate_unique_id()
    await crude_user.add_user(telegram_id=telegram_id, user_name="TestUser")
    result = await crude_user.add_user(telegram_id=telegram_id, user_name="TestUser")
    assert result is True  # True = уже существует


@pytest.mark.asyncio
async def test_get_user_found(crude_user):
    telegram_id = generate_unique_id()
    await crude_user.add_user(telegram_id=telegram_id, user_name="GetTest")
    user = await crude_user.get_user(telegram_id)
    assert user is not None
    assert user.user_name == "GetTest"


@pytest.mark.asyncio
async def test_get_user_not_found(crude_user):
    user = await crude_user.get_user(999999999)
    assert user is None


@pytest.mark.asyncio
async def test_get_all_users(crude_user):
    telegram_id_1 = generate_unique_id()
    telegram_id_2 = generate_unique_id()
    await crude_user.add_user(telegram_id=telegram_id_1, user_name="User1")
    await crude_user.add_user(telegram_id=telegram_id_2, user_name="User2")

    users = await crude_user.get_all_users()
    assert isinstance(users, list)
    assert any(u.telegram_id == telegram_id_1 for u in users)
    assert any(u.telegram_id == telegram_id_2 for u in users)


@pytest.mark.asyncio
async def test_get_users_by_referral_found(crude_user):
    ref_id = generate_unique_id()
    await crude_user.add_user(telegram_id=ref_id, user_name="RefA")
    await crude_user.add_user(telegram_id=generate_unique_id(), user_name="RefB", referral_id=ref_id)
    await crude_user.add_user(telegram_id=generate_unique_id(), user_name="RefC", referral_id=ref_id)

    users = await crude_user.get_users_by_referral(ref_id)
    assert users is not False
    assert len(users) == 2
    assert all(user.referral_id == ref_id for user in users)


@pytest.mark.asyncio
async def test_get_users_by_referral_not_found(crude_user):
    users = await crude_user.get_users_by_referral(999999999)
    assert users is False


@pytest.mark.asyncio
async def test_update_user(crude_user):
    telegram_id = generate_unique_id()
    await crude_user.add_user(telegram_id=telegram_id, user_name="Old", referral_id=1)
    updated = await crude_user.update_user(telegram_id=telegram_id, user_name="New", referral_id=2, balance=10)
    assert updated is True

    user = await crude_user.get_user(telegram_id)
    assert user.user_name == "New"
    assert user.referral_id == 2
    assert user.balance == 10


@pytest.mark.asyncio
async def test_update_user_not_found(crude_user):
    result = await crude_user.update_user(telegram_id=404000000, user_name="Ghost")
    assert result is False


@pytest.mark.asyncio
async def test_count_users(crude_user):
    await crude_user.add_user(telegram_id=generate_unique_id(), user_name="One")
    await crude_user.add_user(telegram_id=generate_unique_id(), user_name="Two")
    count = await crude_user.count_users()
    assert count >= 2


@pytest.mark.asyncio
async def test_count_users_by_referral(crude_user):
    ref_id = generate_unique_id()
    await crude_user.add_user(telegram_id=ref_id, user_name="Origin")
    await crude_user.add_user(telegram_id=generate_unique_id(), user_name="Ref1", referral_id=ref_id)
    await crude_user.add_user(telegram_id=generate_unique_id(), user_name="Ref2", referral_id=ref_id)

    count = await crude_user.count_users_by_referral(ref_id)
    assert count == 2


@pytest.mark.asyncio
async def test_delete_user_found(crude_user):
    telegram_id = generate_unique_id()
    await crude_user.add_user(telegram_id=telegram_id, user_name="ToDelete")
    result = await crude_user.delete_user(telegram_id)
    assert result is True

    user = await crude_user.get_user(telegram_id)
    assert user is None


@pytest.mark.asyncio
async def test_delete_user_not_found(crude_user):
    result = await crude_user.delete_user(987654321)
    assert result is False
