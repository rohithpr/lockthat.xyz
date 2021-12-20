import pytest
from service import account_service
from db import models
from db.models import Account
import uuid


def test_create_account():
    test_account = str(uuid.uuid4())
    with pytest.raises(Account.DoesNotExist):
        account = models.Account.get(test_account)
    created_account = account_service.create_account(test_account)
    account = models.Account.get(test_account)
    assert created_account.uid == account.uid
    assert account.uid == test_account
