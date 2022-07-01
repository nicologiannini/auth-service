from typing import Dict


class DefaultException(Exception):

    code = None

    def __init__(self, message, error_code=None):
        if not message:
            message = type(self).__name__
        self.message = message

        if error_code:
            self.code = error_code

        if self.code:
            super().__init__(f"<Response [{self.code}]> {message}")
        else:
            super().__init__(f"<Response> {message}")


class InvalidRequest(DefaultException):
    code = 400


class Unauthorized(DefaultException):
    code = 401


class NotEnabled(DefaultException):
    code = 402


class ValidationError(DefaultException):
    code = 403


class NotFound(DefaultException):
    code = 404


class TooManyRequests(DefaultException):
    code = 429


class InternalError(DefaultException):
    code = 500


class ServiceUnavailable(DefaultException):
    code = 503


class TimeoutError(DefaultException):
    code = 504


ExceptionMap: Dict[int, DefaultException] = {
    InvalidRequest.code: InvalidRequest,
    Unauthorized.code: Unauthorized,
    NotEnabled.code: NotEnabled,
    TooManyRequests.code: TooManyRequests,
    InternalError.code: InternalError,
    TimeoutError.code: TimeoutError,
    ServiceUnavailable.code: ServiceUnavailable,
}
