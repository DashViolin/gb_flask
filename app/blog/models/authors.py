from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..extensions import db


class Author(db.Model):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow(), onupdate=datetime.utcnow())

    user = relationship("User", back_populates="author")
