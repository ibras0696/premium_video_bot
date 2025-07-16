import pytest
from database import CrudeUser, CrudePayments, CrudeSubscriptions


@pytest.fixture(scope="function")
def crude_user():
    return CrudeUser()


@pytest.fixture(scope="function")
def crude_subscriptions():
    return CrudeSubscriptions()


@pytest.fixture(scope="function")
def crude_payments():
    return CrudePayments()
