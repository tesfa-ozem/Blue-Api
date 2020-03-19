import os
from logging.handlers import RotatingFileHandler

from flask import Flask, request, current_app
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import logging

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    with app.app_context():
        db.create_all()

    from blue.api.routes import mod as mod
    app.register_blueprint(mod)

    from blue.site.routes import mod as mod
    app.register_blueprint(mod)

    from blue.utilities.utilities import mod as mod
    app.register_blueprint(mod)
    if not app.debug and not app.testing:
        # ...

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/microblog.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app


from blue import models
