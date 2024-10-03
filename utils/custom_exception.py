from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class CustomException(Exception):
    def __init__(
        self, message: str, data=None, headers=None, code=None, status_code=None
    ):
        if data is None:
            data = []
        if headers is None:
            headers = {}
        if code is None:
            code = "FAILED"
        if status_code is None:
            status_code = status.HTTP_400_BAD_REQUEST
        self.code = code
        self.message = message
        self.data = data
        self.headers = headers
        self.status_code = status_code


class BadRequestException(CustomException):
    def __init__(self, message: str, data=None, headers=None):
        super().__init__(message, data, headers)
        self.code = "BAD_REQUEST"


class IntegrityException(CustomException):
    def __init__(self, message: str, data=None, headers=None):
        super().__init__(message, data, headers)
        self.code = "INTEGRITY_ERROR"


class NotFoundException(CustomException):
    def __init__(self, message: str, data=None, headers=None):
        super().__init__(message, data, headers)
        self.code = "NOT_FOUND"


class UnAuthorizedException(CustomException):
    def __init__(self, message: str, data=None, headers=None):
        super().__init__(message, data, headers)
        self.code = "UNAUTHORIZED"


def custom_exception_handler(request: Request, exc: CustomException):
    status_code = exc.status_code
    if exc.code == "NOT_FOUND":
        status_code = status.HTTP_404_NOT_FOUND
    elif exc.code == "UNAUTHORIZED":
        status_code = status.HTTP_401_UNAUTHORIZED
    elif exc.code == "CONFLICT":
        status_code = status.HTTP_409_CONFLICT

    return JSONResponse(
        status_code=status_code,
        content={"code": exc.code, "message": exc.message, "data": exc.data},
        headers=exc.headers,
    )


def register_app(app: FastAPI):
    app.add_exception_handler(CustomException, custom_exception_handler)
    app.add_exception_handler(BadRequestException, custom_exception_handler)
    app.add_exception_handler(IntegrityException, custom_exception_handler)
    app.add_exception_handler(NotFoundException, custom_exception_handler)
    app.add_exception_handler(UnAuthorizedException, custom_exception_handler)
