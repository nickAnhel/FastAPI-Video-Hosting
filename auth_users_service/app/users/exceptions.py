class UserNotFound(Exception):
    """User not found exception."""

    def __init__(self, message="User not found"):
        super().__init__(message)

class UserNotInSubscriptions(Exception):
    """User not found exception."""

    def __init__(self, message="User not in subscriptions"):
        super().__init__(message)


class InvalidAuthToken(Exception):
    """Invalid authorization token exception."""

    def __init__(self, message="Invalid authorization token"):
        super().__init__(message)


class CantDeleteUsersVideos(Exception):
    """Can't delete users videos exception."""

    def __init__(self, message="Can't delete users videos"):
        super().__init__(message)


class CantSubscribeToUser(Exception):
    """Can't subscribe exception."""

    def __init__(self, message="Can't subscribe"):
        super().__init__(message)

class CantUnsubscribeFromUser(Exception):
    """Can't unsubscribe exception."""

    def __init__(self, message="Can't subscribe"):
        super().__init__(message)
