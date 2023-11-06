from enum import Enum
from functools import wraps
from http import HTTPStatus
from typing import Any
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import Optional
from typing import Protocol
from typing import Type

import desert
import jwt
from flask import abort
from flask import request
from flask_apispec.annotations import activate
from flask_apispec.annotations import annotate
from marshmallow import Schema

from app.schemas.decorators import JwtToken


class DataClass(Protocol):
    __dataclass_fields__: ClassVar[Dict]


class _RequestLocation(Enum):
    BODY = 'body'
    QUERY = 'query'


def _annotate_request(fn: Callable, Schema: Type[Schema], location: str):
    """Annotate the function `fn`'s request sample with
    the given schema `Schema`. `location` can be set to `body`
    or `query` to assign the annotation to the request body or
    query params respectively. ::

    :param fn: Function to be annotated
    :type fn: Callable
    :param Schema: Schema used to define the structure of
        the sample annotation
    :type Schema: Type[Schema]
    :param location: Where the sample annotation is located, can be
        `body` or `query`
    :type location: str
    :return: Returns the annotated function
    :rtype: Callable
    """
    kwargs = {
        'location': location,
    }
    # Annotate the 'parameters' section of the endpoint in the docs.
    # Use the schema to generate a sample value and set its location
    # to the location argument
    annotate(fn, 'args', [{'args': Schema, 'kwargs': kwargs}], apply=False)
    return activate(fn)


def _annotate_response(
    fn: Callable,
    Schema: Type[Schema],
    status_code: str = 'default',
    description='',
):
    """Annotate `fn`'s responses section with a sample value
    built according to the given `Schema`. `status_code` can be given
    if the expected status code for a successful exection is anything
    other than 200. `description` can be provided to give additional
    details regarding the contents of the response. ::

    :param fn: Function to be annotated
    :type fn: Callable
    :param Schema: Schema used to define the structure of
        the sample annotation
    :type Schema: Type[Schema]
    :param status_code: Status code for the annotated response,
        defaults to "default"
    :type status_code: str, optional
    :param description: Description of the response, defaults to ""
    :type description: str, optional
    :return: Annoatated function
    :rtype: Callable
    """
    options = {
        status_code: {
            'schema': Schema,
            'description': description,
        },
    }
    # Annotate the 'responses' section of the endpoint in the docs.
    # Use the schema to generate a sample value for the response
    #   (with the given status code)
    #   and adds a description for the response, if a description is provided.
    annotate(fn, 'schemas', [options], apply=False)
    return activate(fn)


def request_model(
    body_model: Optional[Type[DataClass]] = None,
    query_model: Optional[Type[DataClass]] = None,
    meta: Dict[str, Any] = {},
    query_meta: Dict[str, Any] = {},
):
    """Deserialize incoming request data and inject the deserialized
    data as additional `kwargs` to the decorated function. `body_model`
    will be used to parse the request body, the body will be injected as the
    `payload` kwarg in the decorated function with the type defined by the
    `body_model` argument. `query_model` can be given in case the function
    expects any query parameters. If `query_model` is given, the query
    parameters will be deserialized and injected to the decorated function
    as the `query_args` kwarg. `body_model` is now also optional,
    since it is possible to use this decorator with GET requests,
    where request bodies would typically be empty anyway.

    The dataclasses are converted to marshmallow Schemas within this function.
    If there are any marshmallow meta classes that need to be defined for the
    request body/query parameters (e.g. 'unknown': marshmallow.EXCUDE), provide
    values for the `meta` and `query_meta` kwargs respectively. ::

    :param body_model: Model used to deserialize the request body. The
        injected `payload` kwarg will be of this type, defaults to None
    :type body_model: Optional[Type[DataClass]], optional
    :param query_model: Model used to deserialize the request body. The
        injected `query_args` kwarg will be of this type, defaults to None
    :type query_model: Optional[Type[DataClass]], optional
    :param meta: Marshmallow meta class params for the
        schema used to validate the request body, defaults to {}
    :type meta: Dict[str, Any], optional
    :param query_meta: Marshmallow meta class params for the
        schema used to validate the query parameters, defaults to {}
    :type query_meta: Dict[str, Any], optional
    """

    def decorator(fn: Callable):
        # Convert the models to marshmallow schemas using desert;
        # used for validation
        Schema = None
        if body_model:
            Schema = desert.schema_class(body_model, meta=meta)
            # Add swagger docs for the body (and query params if needed)
            _annotate_request(fn, Schema, location=_RequestLocation.BODY.value)
        QuerySchema = None
        if query_model:
            QuerySchema = desert.schema_class(query_model, meta=query_meta)
            _annotate_request(
                fn,
                QuerySchema,
                location=_RequestLocation.QUERY.value,
            )

        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not Schema and (request and request.data):
                raise ValueError(
                    (
                        'REQUEST DECORATOR: body_model must be set '
                        'for endpoints that expect request bodies.'
                    ),
                )

            if Schema:
                # Grab the request body and convert it to
                # an object of the type `body_model`
                json_payload = request.get_json()
                processed_payload = Schema().load(json_payload)
                # Inject the deserialized data into the decorated function
                kwargs.update({'payload': processed_payload})
            if QuerySchema:
                # Grab the request query params and convert them to
                # an object of the type `query_model`
                query_args = request.args
                processed_args = QuerySchema().load(query_args)
                # Inject a value for query_args into the decorated function
                kwargs.update({'query_args': processed_args})
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def response_model(
    model: Type[DataClass],
    many: bool = False,
    meta: Dict[str, Any] = {},
    status_code: str = '200',
    doc_description: str = '',
):
    """Serialize outgoing response data according to the given
    `model`. The decorated function is expected to return an object with
    the type of `model`, since `model` will be used
    to serialize the returned data.

    `model` will be converted to a marshmallow Schema to validate the response.
    If there is any marshmallow meta class that needs to be built
    (e.g. `unknown`: marshmallow.EXCLUDE),
    provide a value for `meta`.

    :param model: Model used to deserialize the request body. The
        injected `payload` kwarg will be of this type.
    :type model: Type[DataClass]
    :param many: Whether the response is a list and the given model
        only represents a single item of that list.
        Same as the keyword argument
        `many` in Marshmallow schemas, defaults to False
    :type many: bool, optional
    :param meta: Marshmallow meta class params for the
        schema used to validate the request body, defaults to {}
    :type meta: Dict[str, Any], optional
    :param status_code: Status code for the response upon successful
        execution, defaults to "200"
    :type status_code: str, optional
    :param doc_description: Description used for the response in the Swagger
        documentation, defaults to ""
    :type doc_description: str, optional
    """

    def decorator(fn: Callable):
        # Convert the model to a marshmallow schema using desert;
        # used for validation
        Schema = desert.schema_class(model, meta=meta)
        # Add swagger docs for the response (and query params if needed)
        _annotate_response(
            fn,
            Schema,
            status_code=status_code,
            description=doc_description,
        )

        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Execute the function
            # TODO(avon) fixed mypy issue; ask help from brian
            response: DataClass = fn(*args, **kwargs)  # type: ignore
            # Deserialize the result using the schema built previously
            processed_response = Schema(many=many).dump(response)
            return processed_response

        return wrapper

    return decorator


# Create a decorator that extracts the cookie header and injects it to the
# decorated function
def use_user_token():
    def decorator(fn: Callable):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Grab the cookie header and inject it into the decorated function
            encoded_user_token = request.cookies.get('next-auth.session-token')
            if not encoded_user_token:
                abort(HTTPStatus.UNAUTHORIZED)
            encoded_token_bytes = encoded_user_token.encode('utf-8')
            # JWT Decode the cookie header and inject it into the decorated
            # function
            decoded_user_token = jwt.decode(
                encoded_token_bytes,
                'SECRET_KEY1',
                algorithms=['HS256'],
            )
            jwt_obj = desert.schema(JwtToken).load(decoded_user_token)
            kwargs.update({'user_token': jwt_obj})
            return fn(*args, **kwargs)

        return wrapper

    return decorator
