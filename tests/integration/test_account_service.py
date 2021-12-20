import pytest
from db import models
from db.models import Account
from service import account_service

from .utils import get_uuid


def test_create_account():
    test_account = get_uuid()
    with pytest.raises(Account.DoesNotExist):
        account = models.Account.get(test_account)
    created_account = account_service.create_account(test_account)
    account = models.Account.get(test_account)
    assert created_account.uid == account.uid
    assert account.uid == test_account
