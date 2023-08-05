class BaseException(Exception):
    def __init__(self, message, code):
        self.code = code
        super(BaseException, self).__init__(message)


class ClientError(BaseException):
    def __init__(self, message="", ext=0):
        code = 400 + ext
        super(ClientError, self).__init__(message, code)


class ServerError(BaseException):
    def __init__(self, message="", ext=0):
        code = 500 + ext
        super(ServerError, self).__init__(message, code)
