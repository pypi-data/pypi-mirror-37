class FCMError(Exception):
    """Base FCM Error."""


class FCMMissingRegistration(FCMError):
    """
    Missing registration.
    200
    Check that the request contains a registration token (in the registration_id in a plain text
    message, or in the to or registration_ids field in JSON).
    """


class FCMInvalidRegistration(FCMError):
    """
    Invalid registration.
    200
    Check the format of the registration token you pass to the server. Make sure it matches the
    registration token the client app receives from registering with Firebase Notifications. Do not
    truncate or add additional characters.
    """


class FCMNotRegistered(FCMError):
    """
    Not registered.
    200
    An existing registration token may cease to be valid in a number of scenarios, including:
    * If the client app unregisters with FCM.
    * If the client app is automatically unregistered, which can happen if the user uninstalls the
    application. For example, on iOS, if the APNS Feedback Service reported the APNS token as
    invalid.
    * If the registration token expires (for example, Google might decide to refresh registration
    tokens, or the APNS token has expired for iOS devices).
    * If the client app is updated but the new version is not configured to receive messages.
    For all these cases, remove this registration token from the app server and stop using it to
    send messages.
    """


class FCMInvalidPackageName(FCMError):
    """
    Invalid package name.
    200
    Make sure the message was addressed to a registration token whose package name matches the
    value passed in the request.
    """


class FCMAuthenticationError(FCMError):
    """
    Authentication error.
    401
    The sender account used to send a message couldn't be authenticated. Possible causes are:
    Authorization header missing or with invalid syntax in HTTP request.
    The Firebase project that the specified server key belongs to is incorrect.
    Legacy server keys only—the request originated from a server not whitelisted in the Server key
    IPs.
    Check that the token you're sending inside the Authentication header is the correct Server key
    associated with your project. See Checking the validity of a Server key for details. If you are
    using a legacy server key, you're recommended to upgrade to a new key that has no IP
    restrictions.
    """


class FCMMismatchSenderId(FCMError):
    """
    Mismatch sender_id.
    200
    A registration token is tied to a certain group of senders. When a client app registers for
    FCM, it must specify which senders are allowed to send messages. You should use one of those
    sender IDs when sending messages to the client app. If you switch to a different sender, the
    existing registration tokens won't work.
    """


class FCMInvalidParameters(FCMError):
    """
    Invalid parameters.
    400
    Check that the JSON message is properly formatted and contains valid fields (for instance,
    making sure the right data type is passed in).
    Check that the provided parameters have the right name and type.
    """


class FCMMessageTooBig(FCMError):
    """
    Message too big.
    200
    Check that the total size of the payload data included in a message does not exceed FCM limits:
    4096 bytes for most messages, or 2048 bytes in the case of messages to topics. This includes
    both the keys and the values.
    """


class FCMInvalidDataKey(FCMError):
    """
    Invalid data key.
    200
    Check that the payload data does not contain a key (such as from, or gcm, or any value prefixed
    by google) that is used internally by FCM. Note that some words (such as collapse_key) are also
    used by FCM but are allowed in the payload, in which case the payload value will be overridden
    by the FCM value.
    """


class FCMInvalidTtl(FCMError):
    """
    Invalid TTL.
    200
    Check that the value used in time_to_live is an integer representing a duration in seconds
    between 0 and 2,419,200 (4 weeks).
    """


class FCMUnavailable(FCMError):
    """
    Unavailable.
    5xx or 200
    The server couldn't process the request in time. Retry the same request, but you must:
    Honor the Retry-After header if it is included in the response from the FCM Connection Server.
    Implement exponential back-off in your retry mechanism. (e.g. if you waited one second before
    the first retry, wait at least two second before the next one, then 4 seconds and so on). If
    you're sending multiple messages, delay each one independently by an additional random amount
    to avoid issuing a new request for all messages at the same time.
    Senders that cause problems risk being blacklisted.
    """


class FCMInternalServerError(FCMError):
    """
    Internal server error.
    5xx or 200
    The server encountered an error while trying to process the request. You could retry the same
    request following the requirements listed in "Timeout" (see row above). If the error persists,
    please contact Firebase support.
    """


class FCMDeviceMessageRateExceeded(FCMError):
    """
    Device message rate exceeded.
    200
    The rate of messages to a particular device is too high. If an iOS app sends messages at a rate
    exceeding APNs limits, it may receive this error message
    Reduce the number of messages sent to this device and use exponential backoff to retry sending.
    """


class FCMTopicsMessageRateExceeded(FCMError):
    """
    Topics message rate exceeded.
    200
    The rate of messages to subscribers to a particular topic is too high. Reduce the number of
    messages sent for this topic and use exponential backoff to retry sending.
    """


class FCMInvalidApnsCredential(FCMError):
    """
    Invalid APNS credential.
    200
    A message targeted to an iOS device could not be sent because the required APNs authentication
    key was not uploaded or has expired. Check the validity of your development and production
    credentials.
    """



# class FCMServerError(FCMError):
#     """Internal server error or timeout error on Firebase cloud messaging server."""
#
#
# class FCMInvalidDataError(FCMError):
#     """Invalid input."""
#
#
# class FCMInternalPackageError(FCMError):
#     """JSON parsing error, please create a new github issue describing what you're doing."""
