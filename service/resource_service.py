from datetime import datetime

from dateutil.relativedelta import relativedelta
from misc import exceptions


def create_resource(account, resource_name):
    if resource_name in account.resources:
        raise exceptions.ResourceExistsException()

    account.resources[resource_name] = {}
    account.save()
    return account


def create_resource_acquire_status_message(resource_name, user, expiry, lock_reason, overridden_from=None):
    message = f"Resource '{resource_name}' is locked by user '{user}' till {expiry.strftime('%Y-%b-%d %I:%M %p')} UTC."
    if lock_reason:
        message = f"{message} Reason: {lock_reason}."
    if overridden_from:
        message = f"{message} The resource was acquired by overriding the previous lock held by {overridden_from}."
    return message


def acquire_resource(account, resource_name, user, duration=1440, message="", override=False):
    if resource_name not in account.resources:
        account = create_resource(account, resource_name)

    resource = account.resources[resource_name]
    expiry = datetime.fromisoformat(resource.get("expiry", str(datetime.utcnow())))
    overridden_from = None

    if resource.get("locked", False) and resource.get("user", None) != user and expiry > datetime.utcnow():
        if override:
            overridden_from = resource.get("user")
        else:
            message = create_resource_acquire_status_message(
                resource_name,
                resource["user"],
                expiry,
                resource["message"],
            )
            raise exceptions.ResourceLocked(message)

    expiry = datetime.utcnow() + relativedelta(minutes=duration)
    account.resources[resource_name] = {"locked": True, "user": user, "message": message, "expiry": str(expiry)}
    account.save()
    resource = account.resources[resource_name]
    message = create_resource_acquire_status_message(
        resource_name, resource["user"], expiry, resource["message"], overridden_from
    )
    return account, message
