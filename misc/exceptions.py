class HoldException(Exception):
    """Base class for custom exceptions."""

    def __init__(self, message=""):
        self.message = message


class ResourceExistsException(HoldException):
    pass


class ResourceDoesNotExistException(HoldException):
    pass


class ResourceLocked(HoldException):
    def __init__(self, message=""):
        super().__init__(message)
