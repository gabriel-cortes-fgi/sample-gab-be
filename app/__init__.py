from flask import Flask
from flask_cors import CORS

from . import errors
from . import models
from . import routes


def create_app() -> Flask:
    app = Flask(__name__)
    logger = app.logger
    CORS(
        app,
        supports_credentials=True,
        origins=[
            'https://fgi.local',
            r'^https:\/\/([A-Za-z0-9\-\.]+)\.fgi\.local$',
            'https://localhost',
            'http://localhost',
            r'^https://localhost:(\d){1,5}$',
            r'^http://localhost:(\d){1,5}$',
            'https://webservice-files.s3.amazonaws.com/',
            r'^https:\/\/([A-Za-z0-9\-\.]+)\.app\.focusglobalinc\.com$',
            r'^https:\/\/([A-Za-z0-9\-\.]+)\.ap-southeast-1\
                .awsapprunner\.com$',
            r'^https:\/\/([A-Za-z0-9\-\.]+)\.cloudfront\.net$',
        ],
    )

    # SQLAlchemy
    logger.info('Initializing SQLAlchemy...')
    models.init_db(app)
    # Flask-Marshmallow
    # Important: initialize this **after** SQLAlchemy init
    logger.info('Initializing Flask-Marshmallow...')
    models.init_marshmallow(app)

    # # Flask-JWT-Extended
    # logger.info('Initializing Flask-JWT-Extended...')
    # routes.init_jwt(app)

    # Register blueprints and add resources to `api`
    # Important: Add resources before passing the app object to the api object
    # Reason: Doing it the other way around causes the urls to not be found
    logger.info('Registering routes...')
    routes.register_routes(app)

    # Flask-RESTful
    logger.info('Initializing Flask-RESTful...')
    routes.init_api(app)

    # Flask-APISpec
    logger.info('Initializing Flask-APISpec...')
    routes.init_docs(app)

    # Map errors to responses
    logger.info('Registering error handlers...')
    errors.register_error_handlers(app)

    return app
