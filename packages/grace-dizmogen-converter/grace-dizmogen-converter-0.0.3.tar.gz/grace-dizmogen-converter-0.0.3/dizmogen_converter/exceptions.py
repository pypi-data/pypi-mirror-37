class BaseException(Exception):
    def __init__(self, message):
        super().__init__(message)


class GeneratorDizmoError(BaseException):
    pass


class GraceDizmoError(BaseException):
    pass
