import pytest
from service import account_service
from db import models
from db.models import Account


def test_create_account():
    test_account = "test-account"
    import pudb; pudb.set_trace()
    with pytest.raises(Account.DoesNotExist):
        account = models.Account.get(test_account)
    account_service.create_account(test_account)
    account = models.Account.get(test_account)
    assert account.uid == test_account
