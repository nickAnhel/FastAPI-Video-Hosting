class UserNotFound(Exception):
    """User not found exception."""

    def __init__(self, message="User not found"):
        super().__init__(message)


class UsernameOrEmailAlreadyExists(Exception):
    """Username or email already exists exception."""

    def __init__(self, message="Username or email already exists"):
        super().__init__(message)


class UserNotInSubscriptions(Exception):
    """User not found exception."""

    def __init__(self, message="User not in subscriptions"):
        super().__init__(message)


class CantSubscribeToUser(Exception):
    """Can't subscribe exception."""

    def __init__(self, message="Can't subscribe"):
        super().__init__(message)


class CantUnsubscribeFromUser(Exception):
    """Can't unsubscribe exception."""

    def __init__(self, message="Can't subscribe"):
        super().__init__(message)


class WrongValueOfOrder(Exception):
    """Wrong value of order exception."""

    def __init__(self, message="Wrong value of order"):
        super().__init__(message)


class WrongLimitOrOffset(Exception):
    """Wrong limit or offset exception."""

    def __init__(self, message="Wrong limit or offset"):
        super().__init__(message)


class FailedToDecodeToken(Exception):
    """Wrong limit or offset exception."""

    def __init__(self, message="Failed to decode token"):
        super().__init__(message)
