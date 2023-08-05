from flask import Flask
from template_filters import rus_datetime_fmt

from .articles.views import article
from .index.views import index
from .users.views import user


def register_blueprints(app: Flask):
    app.register_blueprint(index)
    app.register_blueprint(user)
    app.register_blueprint(article)


def register_template_filters(app: Flask):
    app.add_template_filter(rus_datetime_fmt)


def create_app() -> Flask:
    """
    Flask app fabric pattern
    """
    app = Flask(__name__)
    register_blueprints(app)
    register_template_filters(app)
    return app
