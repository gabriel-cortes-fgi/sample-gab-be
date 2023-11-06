import os
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from app.resources.brand import BrandListsResource, BrandResource
from app.extensions import api_v1
from flask import Flask
from app.types.flask import ResourceResponseType
from http import HTTPStatus
from typing import Any
from marshmallow import Schema
from apispec.ext.marshmallow.common import resolve_schema_cls
from app.extensions import docs
from typing import Dict


def register_routes(app: Flask) -> None:
    @app.route('/')
    def check() -> ResourceResponseType:
        return {'message': 'API is working fine!'}, HTTPStatus.OK

    @app.route('/throw_error')
    def check_error_handler() -> Any:
        raise Exception('Error handler works fine!')

    api_v1.add_resource(BrandListsResource, '/brand')
    api_v1.add_resource(BrandResource, '/brand/<int:brand_id>')


_schemas: Dict[str, bool] = {}


def resolve_schema_name(schema: Schema):
    global _schemas

    schema_cls = resolve_schema_cls(schema)
    name = schema_cls.__name__

    if name in _schemas.keys():
        return False

    _schemas[name] = True
    return name


def init_docs(app: Flask) -> None:
    if (
        os.getenv('WEBSERVICE_ENV') != 'localhost'
        or os.getenv('ENABLE_APISPEC', 'false').lower() == 'true'
    ):
        ma_plugin = MarshmallowPlugin(
            schema_name_resolver=resolve_schema_name,  # type: ignore
        )
        app.config.update(
            {
                'APISPEC_SPEC': APISpec(
                    title='WebService Backend',
                    version='v1',
                    plugins=[ma_plugin],
                    openapi_version='2.0.0',
                ),
                'APISPEC_SWAGGER_URL': '/swagger/',
                'APISPEC_SWAGGER_UI_URL': '/swagger-ui/',
            },
        )

    docs.init_app(app)
    docs.register(BrandListsResource)
    docs.register(BrandResource)


def init_api(app: Flask) -> None:
    api_v1.init_app(app)
