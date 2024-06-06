from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager  # Ensure this import is added
from config import Config
import logging
from logging.handlers import SysLogHandler
import os
from flask_compress import Compress
from flask_caching import Cache

db = SQLAlchemy()
migrate = Migrate()
compress = Compress()
cache = Cache()
def setup_logging(app):
    if app.config['FLASK_ENV'] == 'production':  # Only configure logging in production environment
        # Create a SysLogHandler with the appropriate address and port
        try:
            handler = SysLogHandler(address=('logs2.papertrailapp.com', 21658))
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [in %(pathname)s:%(lineno)d] %(message)s')
            handler.setFormatter(formatter)
            app.logger.addHandler(handler)
            app.logger.setLevel(logging.INFO)
        except Exception as e:
            app.logger.error('Failed to setup logging:', exc_info=e)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['CACHE_TYPE'] = 'simple'

    compress.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    setup_logging(app)
    cache.init_app(app)
    jwt = JWTManager(app)  # This initializes JWTManager with the Flask app

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
