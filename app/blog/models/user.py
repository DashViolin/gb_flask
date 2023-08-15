from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Boolean, Column, DateTime, Integer, String

from ..extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(80), unique=False, nullable=False)
    fullname = Column(String(80), unique=False, nullable=False)
    email = Column(String(80), unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    is_staff = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<User #{self.id} {self.username!r}>"
