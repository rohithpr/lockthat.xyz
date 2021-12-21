from db.models import Account


def get_account(account_id):
    return Account.get(account_id)


def create_account(account_id):
    account = Account(uid=account_id)
    account.save()
    return account


def get_or_create_account(account_id):
    try:
        account = get_account(account_id)
    except Account.DoesNotExist:
        account = Account(uid=account_id)
    return account
