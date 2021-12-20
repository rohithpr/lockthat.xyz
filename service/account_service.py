from db.models import Account


def create_account(account_id):
    account = Account(uid=account_id)
    account.save()
    return account
