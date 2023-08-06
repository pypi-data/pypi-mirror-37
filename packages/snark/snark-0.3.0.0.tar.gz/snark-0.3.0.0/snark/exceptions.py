from click import ClickException


class SnarkException(ClickException):

    def __init__(self, message=None, code=None):
        super(SnarkException, self).__init__(message)


class AuthenticationException(SnarkException):

    def __init__(self, message="Authentication failed. Please login again."):
        super(AuthenticationException, self).__init__(message=message)


class AuthorizationException(SnarkException):

    def __init__(self, response):
        try:
            message = response.json()["message"]
        except (KeyError, AttributeError):
            message = "You are not authorized to access this resource on Snark AI."
        super(AuthorizationException, self).__init__(message=message)


class NotFoundException(SnarkException):

    def __init__(self, message="The resource you are looking for was not found. Check if the name or id is correct."):
        super(NotFoundException, self).__init__(message=message)


class BadRequestException(SnarkException):

    def __init__(self, response):
        try:
            message = "One or more request parameters is incorrect\n%s" % response.json()['message']
        except (KeyError, AttributeError):
            message = "One or more request parameters is incorrect, %s" % response.content
        super(BadRequestException, self).__init__(message=message)


class OverLimitException(SnarkException):

    def __init__(self, message="You are over the allowed limits for this operation. Consider upgrading your account."):
        super(OverLimitException, self).__init__(message=message)


class ServerException(SnarkException):

    def __init__(self, message="Internal Snark AI server error."):
        super(ServerException, self).__init__(message=message)


class BadGatewayException(SnarkException):

    def __init__(self, message="Invalid response from Snark AI server."):
        super(BadGatewayException, self).__init__(message=message)


class GatewayTimeoutException(SnarkException):

    def __init__(self, message="Snark AI server took too long to respond."):
        super(GatewayTimeoutException, self).__init__(message=message)


class WaitTimeoutException(SnarkException):

    def __init__(self, message="Timeout waiting for server state update."):
        super(WaitTimeoutException, self).__init__(message=message)


class LockedException(SnarkException):

    def __init__(self, message="Resource locked."):
        super(LockedException, self).__init__(message=message)
