class HoldException(Exception):
    """Base class for custom exceptions."""

    pass


class ResourceExistsException(HoldException):
    pass
