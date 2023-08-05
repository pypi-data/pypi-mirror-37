class FCMError(Exception):
    """Base FCM Error."""


class FCMAuthenticationError(FCMError):
    """API key not found or there was an error authenticating the sender."""


class FCMServerError(FCMError):
    """Internal server error or timeout error on Firebase cloud messaging server."""


class FCMInvalidDataError(FCMError):
    """Invalid input."""


class FCMInternalPackageError(FCMError):
    """JSON parsing error, please create a new github issue describing what you're doing."""
