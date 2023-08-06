#Exceptions code to description map
EXCEPTIONS_MAP = dict(enumerate(['Wrong password/login',
                                 '401 Unauthorized',
                                 'Internet issues',
                                 'Blocked'], 1))


class VKApiException(Exception):
    """Superclass"""

    pass


class NetworkException(VKApiException):
    """Raised when HTTP or low-level network errors are thrown"""

    def __init__(self, error, error_code=-1):
        self.code = error_code
        super().__init__(self, str(error))


class AuthException(VKApiException):
    """Raised when having trouble with token getting"""

    def __init__(self, login, passw, error_code):
        self.code = error_code
        error = '''
AuthException: {},
Arguments: login "{}", pass "{}",
'''.format(EXCEPTIONS_MAP[error_code], login, passw, client, scope)
        super().__init__(self, error)


class MethodException(VKApiException):
    """Raised when VKApi returns 'error' field in response"""

    def __init__(self, error):
        super().__init__(self, str(error))
