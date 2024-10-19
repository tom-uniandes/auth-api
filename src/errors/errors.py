from http import HTTPStatus

class ApiError(Exception):
    code = HTTPStatus.UNPROCESSABLE_ENTITY
    description = "Ops!, something is wrong, check and try again"