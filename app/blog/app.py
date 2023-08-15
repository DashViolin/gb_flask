from flask import Flask

from .commands import create_superuser, create_users, init_db
from .config.settings import Config
from .extensions import db, login_manager, migrate
from .middleware import after_request_timestamp, before_request_timestamp
from .template_filters import rus_datetime_fmt
from .views import articles_app, auth_app, index_app, users_app


def register_blueprints(app: Flask):
    app.register_blueprint(auth_app)
    app.register_blueprint(index_app)
    app.register_blueprint(users_app)
    app.register_blueprint(articles_app)


def register_template_filters(app: Flask):
    app.add_template_filter(rus_datetime_fmt)


def register_extensions(app: Flask):
    from .models import User

    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    login_manager.login_view = "auth_app.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: int):
        return User.query.get(int(user_id))


def register_commands(app: Flask):
    app.cli.add_command(init_db)
    app.cli.add_command(create_users)
    app.cli.add_command(create_superuser)


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

    return app
