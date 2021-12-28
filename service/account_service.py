import requests
from db.models import Account
from flask import redirect
from misc import constants


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


def handle_oauth(request):
    args = request.args
    code = args.get("code")
    resp = requests.post(
        "https://slack.com/api/oauth.v2.access",
        data={
            "code": code,
            "client_id": constants.SLACK_CLIENT_ID,
            "client_secret": constants.SLACK_CLIENT_SECRET,
        },
    )
    data = resp.json()
    if not data.get("ok", False):
        return {"message": "The app could not be installed correctly. Please try again."}
    team = data.get("team")
    account_id = team.get("id")
    account_name = team.get("name")
    access_token = data.get("access_token")
    get_or_create_account(account_id=account_id, account_domain=account_name, access_token=access_token)
    redirect_url = f"https://app.slack.com/client/{account_id}"
    return redirect(redirect_url, code=302)
