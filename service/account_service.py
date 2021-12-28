from db.models import Account


def get_account(account_id):
    return Account.get(account_id)


def create_account(account_id, account_domain="", access_token=""):
    account = Account(uid=account_id, account_domain=account_domain, access_token=access_token)
    account.save()
    return account


def get_or_create_account(account_id, account_domain="", access_token=""):
    try:
        account = get_account(account_id)
        if account.account_domain != account_domain:
            account.account_domain = account_domain
            account.save()
        if access_token and account.access_token != access_token:
            account.access_token = access_token
            account.save()
    except Account.DoesNotExist:
        account = Account(uid=account_id, account_domain=account_domain, access_token=access_token)
        account.save()
    return account
