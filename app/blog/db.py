from flask import g
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def close_db(e=None):
    db_ = g.pop("db", None)
    if db_ is not None:
        db_.close()


__all__ = [
    "db",
]
