class eLampClientError(Exception):
    """
    Base exception for all errors raised by the eLampClient library
    """
    def __init__(self, msg=None):
        if msg is None:
            # default error message
            msg = "An error occurred in the eLampClient library"
        super(eLampClientError, self).__init__(msg)


class ParseResponseError(eLampClientError, ValueError):
    """
    Error raised when responses to Web API methods cannot be parsed as valid JSON
    """
    def __init__(self, response_body, original_exception):
        super(ParseResponseError, self).__init__(
            "eLamp API response body could not be parsed: {0}. Original exception: {1}".format(
                response_body, original_exception
            )
        )
        self.response_body = response_body
        self.original_exception = original_exception


class eLampClientNotAuthedError(eLampClientError, ValueError):
    """
    Error raised when responses returns an not authed exception
    """
    def __init__(self, response_body):
        super(eLampClientNotAuthedError, self).__init__(
            "eLamp client is not authed: {0}".format(response_body)
        )
        self.response_body = response_body


class eLampClientInvalidCredentialsError(eLampClientError, ValueError):
    """
    Error raised when responses returns an not authed exception
    """
    def __init__(self, response_body):
        super(eLampClientInvalidCredentialsError, self).__init__(
            "invalid credentials were provided: {0}".format(response_body)
        )
        self.response_body = response_body


class eLampClientUnsufficentScopesError(eLampClientError, ValueError):
    """
    Error raised when api client has unsufficent scopes exception
    """
    def __init__(self, response_body):
        super(eLampClientUnsufficentScopesError, self).__init__(
            "eLamp client has unsufficent scopes: {0}".format(response_body)
        )
        self.response_body = response_body