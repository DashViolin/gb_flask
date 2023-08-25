from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(255), unique=False, nullable=False)
    fullname = Column(String(80), unique=False, nullable=False)
    email = Column(String(80), unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow(), onupdate=datetime.utcnow())
    last_login = Column(DateTime, nullable=True)
    is_staff = Column(Boolean, nullable=False, default=False)

    author = relationship("Author", uselist=False, back_populates="user")

    def __init__(
        self,
        username: str,
        password: str,
        email: str,
        fullname: str,
        id: int = None,
        is_staff: bool = False,
        created_at: datetime = None,
    ):
        if id:
            self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.fullname = fullname
        self.is_staff = is_staff
        self.created_at = created_at

    def __repr__(self):
        return f"<User #{self.id} {self.username!r}>"

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def validate_password(self, password) -> bool:
        return check_password_hash(self.password, password)
