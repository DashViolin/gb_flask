from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from ..extensions import db


class Article(db.Model):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    is_published = Column(Boolean, nullable=False, default=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    author = relationship("User", backref="articles")

    def __repr__(self):
        return f"<Article #{self.id} {self.title}>"
