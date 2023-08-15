from flask import redirect, url_for
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

login_manager = LoginManager()

migrate = Migrate()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth_app.login"))


__all__ = [
    "db",
    "login_manager",
    "migrate",
]
