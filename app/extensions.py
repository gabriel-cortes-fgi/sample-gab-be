# Ignore packages that don't have type stubs for now
from flask_apispec import FlaskApiSpec  # type: ignore
from flask_marshmallow import Marshmallow  # type: ignore
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
api_v1 = Api(prefix='/v1')
ma = Marshmallow()
docs = FlaskApiSpec()
migrate = Migrate(compare_type=True)
