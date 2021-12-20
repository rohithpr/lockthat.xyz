import uuid

import pytest
from misc import exceptions
from service import account_service as sa
from service import resource_service as sr


def test_create_resource():
    uid = str(uuid.uuid4())
    resource_name_1 = str(uuid.uuid4())
    resource_name_2 = str(uuid.uuid4())
    account = sa.create_account(uid)
    sr.create_resource(account, resource_name_1)
    account = sr.create_resource(account, resource_name_2)
    assert account.resources == {resource_name_1: {}, resource_name_2: {}}


def test_create_duplicate_resource():
    uid = str(uuid.uuid4())
    resource_name_1 = str(uuid.uuid4())
    account = sa.create_account(uid)
    sr.create_resource(account, resource_name_1)
    with pytest.raises(exceptions.ResourceExistsException):
        sr.create_resource(account, resource_name_1)


def test_acquire_resource():
    account_id = str(uuid.uuid4())
    resource_name_1 = str(uuid.uuid4())
    resource_name_2 = str(uuid.uuid4())
    user_1 = str(uuid.uuid4())
    user_2 = str(uuid.uuid4())
    account = sa.create_account(account_id)
    sr.create_resource(account, resource_name_1)

    # Acquire a created resource
    account, message_1 = sr.acquire_resource(account, resource_name_1, user_1)
    # TODO: use freeze time fixture instead of checking for startswith
    assert message_1.startswith(f"Resource '{resource_name_1}' is locked by user '{user_1}' till")

    # Create an acquire a resource
    account, message_2 = sr.acquire_resource(account, resource_name_2, user_2)
    assert message_2.startswith(f"Resource '{resource_name_2}' is locked by user '{user_2}' till")


def test_acquire_locked_resource():
    account_id = str(uuid.uuid4())
    resource_name_1 = str(uuid.uuid4())
    user_1 = str(uuid.uuid4())
    user_2 = str(uuid.uuid4())
    account = sa.create_account(account_id)

    account, message_1 = sr.acquire_resource(account, resource_name_1, user_1)

    # A different user should not be able to acquire the lock
    with pytest.raises(exceptions.ResourceLocked):
        account, message_2 = sr.acquire_resource(account, resource_name_1, user_2)

    # The same user should be able to reacquire the lock
    account, message_3 = sr.acquire_resource(account, resource_name_1, user_1, -100, "hello")
    assert message_3.endswith("Reason: hello.")

    # A user should be able to acquire a lock that has expired
    account, message_4 = sr.acquire_resource(account, resource_name_1, user_2)
    assert account.resources[resource_name_1]["user"] == user_2

    # A user should be able to override an existing lock
    with pytest.raises(exceptions.ResourceLocked):
        sr.acquire_resource(account, resource_name_1, user_1)
    account, message_5 = sr.acquire_resource(account, resource_name_1, user_1, override=True)
    assert f"The resource was acquired by overriding the previous lock held by {user_2}." in message_5