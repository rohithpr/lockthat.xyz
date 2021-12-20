from db.models import Account

def create_account(uid):
    account = Account(uid=uid)
    account.save()
