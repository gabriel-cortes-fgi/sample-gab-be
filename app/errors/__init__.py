from http import HTTPStatus

from flask import Flask
from jwt import DecodeError
from jwt import InvalidSignatureError
from marshmallow import ValidationError

from app.types.flask import ResourceResponseType


# Make relevant generic HTTP error classes
class HTTPError(Exception):
    def __init__(
            self,
            *args,
            name: str = 'Generic Error',
            code=500,
            description='',
            **kwargs,
    ):
        self.name = name
        self.code = code
        self.description = description
        return super().__init__(description or name, *args, **kwargs)


class ResourceNotFoundError(HTTPError):
    def __init__(self, name='NOT FOUND', description: str = ''):
        return super().__init__(
            code=HTTPStatus.NOT_FOUND,
            name=name,
            description=description,
        )


class ResourceConflictError(HTTPError):
    def __init__(self, name='CONFLICT', description: str = ''):
        return super().__init__(
            code=HTTPStatus.CONFLICT,
            name=name,
            description=description,
        )


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(DecodeError)
    def jwt_decode_error(exception: DecodeError):
        (message,) = exception.args
        unhandled_code = 'Unhandled JWT Error'
        error_code = unhandled_code

        if isinstance(exception, InvalidSignatureError):
            error_code = 'Signature Verification Failed'
        else:
            # TODO(ghelo) this is being covered, unsure why its not reported
            if message == 'Not enough segments':  # pragma: no cover
                error_code = 'Not Enough JWT Segments'

        status_code = (
            HTTPStatus.INTERNAL_SERVER_ERROR
            if error_code == unhandled_code else
            HTTPStatus.BAD_REQUEST
        )
        return {
            'error': error_code,
            'description': message,
        }, status_code

    @app.errorhandler(HTTPError)
    def not_found_error(e: HTTPError) -> ResourceResponseType:
        return {
            'error': e.name,
            'description': e.description,
        }, e.code

    @app.errorhandler(ValidationError)
    def invalid_payload(e: ValidationError):
        return {
            'error': 'BAD REQUEST',
            'messages': e.messages,
        }, HTTPStatus.BAD_REQUEST

    # Always put this handler last; this is the most generic error handler
    @app.errorhandler(Exception)
    def generic_error(e: Exception) -> ResourceResponseType:
        return {
            'error': 'Generic Error',
            'description': str(e),
        }, HTTPStatus.INTERNAL_SERVER_ERROR
