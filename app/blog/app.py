import os
import pathlib

from dotenv import load_dotenv
from flask import Flask

from .commands import create_users, init_db
from .db import db
from .template_filters import rus_datetime_fmt
from .views import articles_app, auth_app, index_app, login_manager, users_app


def register_blueprints(app: Flask):
    app.register_blueprint(auth_app)
    app.register_blueprint(index_app)
    app.register_blueprint(users_app)
    app.register_blueprint(articles_app)


def register_template_filters(app: Flask):
    app.add_template_filter(rus_datetime_fmt)


def register_config(app: Flask):
    cwd = pathlib.Path(__file__).resolve().parent
    env_path = cwd / r"env/.env"
    load_dotenv(env_path)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


def register_commands(app: Flask):
    app.cli.add_command(init_db)
    app.cli.add_command(create_users)


def create_app() -> Flask:
    """
    Flask app fabric pattern
    """
    app = Flask(__name__)
    register_config(app)
    db.init_app(app)
    register_commands(app)
    register_blueprints(app)
    register_template_filters(app)
    login_manager.init_app(app)
    return app
