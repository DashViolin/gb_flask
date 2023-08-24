from .articles import articles_app
from .auth import auth_app
from .authors import authors_app
from .index import index_app
from .users import users_app

__all__ = [
    "auth_app",
    "users_app",
    "index_app",
    "articles_app",
    "authors_app",
]
