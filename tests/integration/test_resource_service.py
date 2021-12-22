import pytest
from misc import constants, exceptions
from service import account_service as sa
from service import resource_service as sr

from .utils import get_uuid


def test_create_resource():
    account_id = get_uuid()
    resource_name_1 = get_uuid()
    resource_name_2 = get_uuid()
    account = sa.create_account(account_id)
    sr.create_resource(account, resource_name_1)
    message = sr.create_resource(account, resource_name_2)
    assert message == f"The resource {resource_name_2} has been created."
    assert account.resources == {resource_name_1: {}, resource_name_2: {}}


def test_create_duplicate_resource():
    account_id = get_uuid()
    resource_name_1 = get_uuid()
    account = sa.create_account(account_id)
    sr.create_resource(account, resource_name_1)
    with pytest.raises(exceptions.ResourceExistsException):
        sr.create_resource(account, resource_name_1)


def test_resource_creation_limit():
    account_id = get_uuid()
    account = sa.create_account(account_id)
    for i in range(constants.HOBBY_TIER_RESOURCE_LIMIT):
        sr.create_resource(account, get_uuid())
    with pytest.raises(exceptions.ResourceLimitExceededException):
        sr.create_resource(account, get_uuid())


def test_acquire_resource():
    account_id = get_uuid()
    resource_name_1 = get_uuid()
    resource_name_2 = get_uuid()
    user_1 = get_uuid()
    user_2 = get_uuid()
    account = sa.create_account(account_id)
    sr.create_resource(account, resource_name_1)

    # Acquire a created resource
    message_1 = sr.acquire_resource(account, resource_name_1, user_1)
    # TODO: use freeze time fixture instead of checking for startswith
    assert message_1.startswith(f"Resource `{resource_name_1}` is locked by user <@{user_1}> till")

    # Create an acquire a resource
    message_2 = sr.acquire_resource(account, resource_name_2, user_2)
    assert message_2.startswith(f"Resource `{resource_name_2}` is locked by user <@{user_2}> till")


def test_acquire_locked_resource():
    account_id = get_uuid()
    resource_name_1 = get_uuid()
    user_1 = get_uuid()
    user_2 = get_uuid()
    account = sa.create_account(account_id)

    sr.acquire_resource(account, resource_name_1, user_1)

    # A different user should not be able to acquire the lock
    with pytest.raises(exceptions.ResourceLocked):
        sr.acquire_resource(account, resource_name_1, user_2)

    # The same user should be able to reacquire the lock
    message_3 = sr.acquire_resource(account, resource_name_1, user_1, -100, "hello")
    assert message_3.endswith("Reason: hello.")

    # A user should be able to acquire a lock that has expired
    sr.acquire_resource(account, resource_name_1, user_2)
    assert account.resources[resource_name_1]["user"] == user_2

    # A user should be able to override an existing lock
    with pytest.raises(exceptions.ResourceLocked):
        sr.acquire_resource(account, resource_name_1, user_1)
    message_5 = sr.acquire_resource(account, resource_name_1, user_1, override=True)
    assert f"The resource was acquired by overriding the previous lock held by <@{user_2}>." in message_5


def test_release_locked_resource():
    account_id = get_uuid()
    resource_name_1 = get_uuid()
    user_1 = get_uuid()
    user_2 = get_uuid()
    account = sa.create_account(account_id)

    sr.acquire_resource(account, resource_name_1, user_1)
    assert account.resources[resource_name_1] != {}

    with pytest.raises(exceptions.ResourceLocked) as ex:
        sr.release_resource(account, resource_name_1, user_2)
    assert ex.value.message.startswith("You cannot release a lock held by another user. ")

    message_2 = sr.release_resource(account, resource_name_1, user_1)
    assert message_2 == f"The resource `{resource_name_1}` has been released."
    account = sa.get_account(account_id)
    assert account.resources[resource_name_1] == {}


def test_release_unlocked_resource():
    account_id = get_uuid()
    resource_name_1 = get_uuid()
    user_1 = get_uuid()
    user_2 = get_uuid()
    account = sa.create_account(account_id)

    sr.acquire_resource(account, resource_name_1, user_1, duration=-100)
    assert account.resources[resource_name_1] != {}

    message_2 = sr.release_resource(account, resource_name_1, user_2)
    assert message_2 == f"The resource `{resource_name_1}` has been released."
    account = sa.get_account(account_id)
    assert account.resources[resource_name_1] == {}


def test_release_non_existant_resource():
    account_id = get_uuid()
    resource_name_1 = get_uuid()
    user_1 = get_uuid()
    account = sa.create_account(account_id)

    with pytest.raises(exceptions.ResourceDoesNotExistException):
        sr.release_resource(account, resource_name_1, user_1)


def test_list_resources():
    account_id = get_uuid()
    resource_name_1 = "ABC"
    resource_name_2 = "DEF"
    user_1 = get_uuid()
    account = sa.create_account(account_id)
    sr.create_resource(account, resource_name_1)

    response = sr.list_resources(account)
    list_of_resources = response["blocks"][0]["text"]["text"]
    assert f"{resource_name_1}" in list_of_resources

    sr.acquire_resource(account, resource_name_2, user_1)
    response = sr.list_resources(account)
    list_of_resources = response["blocks"][0]["text"]["text"]
    assert f"{resource_name_1}" in list_of_resources and f"{resource_name_2}" in list_of_resources


def test_delete_resource():
    account_id = get_uuid()
    resource_name_1 = get_uuid()
    resource_name_2 = get_uuid()
    user_1 = get_uuid()
    account = sa.create_account(account_id)
    sr.create_resource(account, resource_name_1)
    sr.create_resource(account, resource_name_2)

    assert resource_name_1 in account.resources
    assert resource_name_2 in account.resources

    message_1 = sr.delete_resource(account, resource_name_1, user_1)
    assert message_1 == f"The resource `{resource_name_1}` has been deleted."

    assert resource_name_1 not in account.resources
    assert resource_name_2 in account.resources
