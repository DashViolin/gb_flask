from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import relationship

from ..extensions import db
from .articles_tags import article_tag_association_table


class Article(db.Model):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow(), server_default=func.now())
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow(), onupdate=datetime.utcnow())
    is_published = Column(Boolean, nullable=False, default=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    author = relationship("Author", backref="articles")
    tags = relationship("Tag", secondary=article_tag_association_table, back_populates="articles")

    def __repr__(self):
        return f"<Article #{self.id} {self.title}>"
