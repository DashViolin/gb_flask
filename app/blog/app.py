from flask import Flask

from .admin import admin
from .api import init_api
from .commands import create_superuser, create_tags, init_db, initialize_db_objects, load_fixtures
from .config.settings import Config
from .extensions import db, login_manager, migrate
from .middleware import after_request_timestamp, before_request_timestamp
from .security import flask_bcrypt
from .template_filters import rus_datetime_fmt
from .views import articles_app, auth_app, authors_app, index_app, users_app


def register_blueprints(app: Flask):
    app.register_blueprint(auth_app)
    app.register_blueprint(index_app)
    app.register_blueprint(users_app)
    app.register_blueprint(authors_app)
    app.register_blueprint(articles_app)


def register_template_filters(app: Flask):
    app.add_template_filter(rus_datetime_fmt)


def register_extensions(app: Flask):
    from .models import User

    db.init_app(app)
    db.app = app
    migrate.init_app(app, db, compare_type=True)
    flask_bcrypt.init_app(app)
    login_manager.login_view = "auth_app.login"
    login_manager.init_app(app)
    admin.init_app(app)
    init_api(app)

    @login_manager.user_loader
    def load_user(user_id: int):
        return User.query.get(int(user_id))


def register_commands(app: Flask):
    app.cli.add_command(init_db)
    app.cli.add_command(load_fixtures)
    app.cli.add_command(create_superuser)
    app.cli.add_command(create_tags)


def register_middleware(app: Flask):
    app.before_request(before_request_timestamp)
    app.after_request(after_request_timestamp)


def register_error_handlers(app: Flask):
    @app.errorhandler(404)
    def handler_404(error_msg):
        app.logger.error(error_msg)
        if not app.debug:
            return "Not found!", 404
        return f"{error_msg}", 404

    @app.errorhandler(403)
    def handler_403(error_msg):
        app.logger.error(error_msg)
        if not app.debug:
            return "Forbidden!", 403
        return f"{error_msg}", 403

    @app.errorhandler(Exception)
    def handle_zero_division_error(error):
        app.logger.exception(error)
        return "Error!", 500


def create_app() -> Flask:
    """
    Flask app fabric pattern
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    if Config.DEBUG:
        print(f" * DATABASE: {Config.SQLALCHEMY_DATABASE_URI}")
    register_extensions(app)  # must be first

    register_blueprints(app)
    register_commands(app)
    register_template_filters(app)
    register_middleware(app)
    register_error_handlers(app)

    initialize_db_objects()

    return app
