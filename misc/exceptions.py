class HoldException(Exception):
    """Base class for custom exceptions."""

    def __init__(self, message=""):
        self.message = message


class ResourceExistsException(HoldException):
    pass


class ResourceLimitExceededException(HoldException):
    def __init__(self, message=""):
        super().__init__(message)


class ResourceDoesNotExistException(HoldException):
    def __init__(self, message=""):
        super().__init__(message)


class ResourceLocked(HoldException):
    def __init__(self, message=""):
        super().__init__(message)
