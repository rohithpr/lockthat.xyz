from datetime import datetime

from dateutil.relativedelta import relativedelta
from misc import constants, exceptions


def create_resource(account, resource_name, **_):
    if resource_name in account.resources:
        raise exceptions.ResourceExistsException()

    if account.plan == constants.HOBBY_TIER and len(account.resources) >= constants.HOBBY_TIER_RESOURCE_LIMIT:
        raise exceptions.ResourceLimitExceededException(
            f"The hobby tier only supports {constants.HOBBY_TIER_RESOURCE_LIMIT} resources. "
            "Please delete some existing resources or upgrade to the paid plan."
        )

    account.resources[resource_name] = {}
    account.save()
    return f"The resource {resource_name} has been created."


def create_resource_acquire_status_message(resource_name, user, expiry, lock_message, overridden_from=None):
    lock_reason = "."
    if lock_message:
        lock_reason = f". Reason: {lock_message.rstrip('.')}."

    message = (
        f"Resource `{resource_name}` is locked by user <@{user}> till "
        f"`<!date^{expiry.strftime('%s')}^{{time}} {{date_short_pretty}}|"
        f"{expiry.strftime('%Y-%b-%d %I:%M %p')} UTC>`"
        f"{lock_reason}"
    )
    if overridden_from:
        message = f"{message} The resource was acquired by overriding the previous lock held by <@{overridden_from}>."
    return message


def acquire_resource(account, resource_name, user, duration=1440, message="", override=False):
    if resource_name not in account.resources:
        create_resource(account, resource_name)

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
    return message


def release_resource(account, resource_name, user):
    if resource_name not in account.resources:
        raise exceptions.ResourceDoesNotExistException(message=f"The resource {resource_name} does not exist.")

    resource = account.resources[resource_name]
    expiry = datetime.fromisoformat(resource.get("expiry", str(datetime.utcnow())))
    if resource.get("locked", False) and resource.get("user", None) != user and expiry > datetime.utcnow():
        message = create_resource_acquire_status_message(
            resource_name,
            resource["user"],
            expiry,
            resource["message"],
        )
        message = f"You cannot release a lock held by another user. {message}"
        raise exceptions.ResourceLocked(message)

    account.resources[resource_name] = {}
    account.save()
    return f"The resource `{resource_name}` has been released."


def list_resources(account, **_):
    resources = list(sorted(account.resources.keys()))
    if not resources:
        return "No resources have been registered with the `lockthat` app. Run `/lockthat help` to get started."

    message = (
        f"The following {'resources have' if len(resources) > 1 else 'resource has'}"
        "been registered with the `lockthat` app:\n"
    )
    for resource_name in resources:
        resource = account.resources[resource_name]

        resource_lock_info = ""

        resource_locked = resource.get("locked", False)
        expiry = datetime.fromisoformat(resource.get("expiry", str(datetime.utcnow())))
        if resource_locked and expiry > datetime.utcnow():
            lock_reason = ""
            if resource["message"]:
                lock_reason = f". Reason: {resource['message'].rstrip('.')}."
            resource_lock_info = (
                ": Locked till "
                f"`<!date^{expiry.strftime('%s')}^{{time}} {{date_short_pretty}}|"
                f"{expiry.strftime('%Y-%b-%d %I:%M %p')} UTC>`"
                f" by <@{resource['user']}>"
                f"{lock_reason}"
            )

        resource_line = f"- `{resource_name}`{resource_lock_info}\n"
        message += resource_line

    return {"blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": message}}]}


def help_(**_):
    help_text = (
        "Hello! You can use the following commands with the `lockthat` app:\n"
        "- `/lockthat help`: Display this help text.\n"
        "- `/lockthat create my-resource`: Register a new resource called `my-resource` with the lockthat app.\n"
        "- `/lockthat list`: List all resources.\n"
        "- `/lockthat lock my-resource`: Lock `my-resource` for 24 hours.\n"
        "- `/lockthat lock my-resource 12 d super secret project`: Lock `my-resource` for 12 days and mention"
        " that you're working on a super secret project. "
        "You can lock a resource for a specified amount time such as `30 mins`, `2 hours`, `5 weeks`, or `1 month`.\n"
        "- `/lockthat unlock my-resource`: Unlock `my-resource` and allow others to lock it!\n"
        "- `/lockthat delete my-resource`: Deregister `my-resource` from the lockthat app.\n"
    )
    return {"blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": help_text}}]}


def delete_resource(account, resource_name, user):
    release_resource(account, resource_name, user)
    del account.resources[resource_name]
    account.save()
    return f"The resource `{resource_name}` has been deleted."
