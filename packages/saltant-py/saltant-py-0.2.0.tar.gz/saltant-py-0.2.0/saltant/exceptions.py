"""Contains exceptions used throughout the program."""


class BadEnvironmentError(Exception):
    """The user has an improperly configured environment."""

    pass


class BadHttpRequestError(Exception):
    """Something bad happened with the HTTP request."""

    pass


class AuthenticationError(BadHttpRequestError):
    """The authentication provided was invalid."""

    pass
