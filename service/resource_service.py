from misc import exceptions


def create_resource(account, resource_name):
    if resource_name in account.resources:
        raise exceptions.ResourceExistsException()

    account.resources[resource_name] = {}
    account.save()
    return account
