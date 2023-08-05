class BaseException(Exception):
    def __init__(self, message, code):
        self.code = code
        super(BaseException, self).__init__(message)