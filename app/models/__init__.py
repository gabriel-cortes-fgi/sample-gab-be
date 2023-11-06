import os

from flask import Flask

from app.extensions import db
from app.extensions import ma
from app.extensions import migrate


def init_db(app: Flask) -> None:
    env_conn_string = os.getenv('DB_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        env_conn_string
    )

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.brand import Brand  # noqa: F401


def init_marshmallow(app: Flask) -> None:
    ma.init_app(app)
