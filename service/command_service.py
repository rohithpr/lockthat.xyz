from misc import exceptions

from .resource_service import acquire_resource, create_resource, delete_resource, list_resources, release_resource

TARGETS = {
    "create": create_resource,
    "lock": acquire_resource,
    "unlock": release_resource,
    "release": release_resource,
    "list": list_resources,
    "delete": delete_resource,
}


# TODO: Refactor
def parse_command(text):  # noqa: C901
    fully_invalid_command_message = (
        "Please enter a valid command such as: `list`, `create resource-name`, "
        "`lock resource-name`, `unlock resource-name`, `delete resource-name`"
    )
    args = {}

    words = text.split()
    if not words:
        raise exceptions.InvalidCommand(fully_invalid_command_message)

    command = words[0]
    if command in {"list"}:
        return TARGETS[command], args

    elif command in {"create", "release", "delete", "lock", "unlock"}:
        if not words[1:]:
            raise exceptions.InvalidCommand(fully_invalid_command_message)

    else:
        raise exceptions.InvalidCommand(fully_invalid_command_message)

    args["resource_name"] = words[1]
    if command in {"lock"}:
        words = words[2:]
        if words:
            if words[-1] == "override":
                args["override"] = True
                words = words[:-1]
        if words:
            if words[0].isdigit():
                duration = int(words[0])
            if words[1:]:
                if words[1] in {"m", "min", "mins", "minutes", "minute"}:
                    duration = duration
                elif words[1] in {"h", "hour", "hours"}:
                    duration = duration * 60
                elif words[1] in {"d", "day", "days"}:
                    duration = duration * 60 * 24
                elif words[1] in {"w", "week", "weeks"}:
                    duration = duration * 60 * 24 * 7
                elif words[1] in {"month", "months"}:
                    duration = duration * 60 * 24 * 30
            args["duration"] = duration

        if words[2:]:
            args["message"] = " ".join(words[2:])

    return TARGETS[command], args
