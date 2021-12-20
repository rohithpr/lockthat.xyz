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
