from http import HTTPStatus

class ApiError(Exception):
    code = HTTPStatus.UNPROCESSABLE_ENTITY

    def __init__(self, description="Lo sentimos! ha ocurrido un error, intentelo nuevamente"):
        self.description = description

class Conflict(ApiError):
    code = HTTPStatus.CONFLICT

class Unavailable(ApiError):
    code = HTTPStatus.SERVICE_UNAVAILABLE

class Bad_Request(ApiError):
    code = HTTPStatus.BAD_REQUEST