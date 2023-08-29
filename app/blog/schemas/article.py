from combojsonapi.utils import Relationship
from marshmallow_jsonapi import Schema
from marshmallow_jsonapi.fields import DateTime, Integer, String


class ArticleSchema(Schema):
    class Meta:
        type_ = "article"
        self_view = "article_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "article_list"

    id = Integer(as_string=True)
    title = String(allow_none=False)
    body = String(allow_none=False)
    dt_created = DateTime(allow_none=False)
    dt_updated = DateTime(allow_none=False)
    author = Relationship(
        nested="AuthorSchema",
        attribute="author",
        related_view="author_detail",
        related_view_kwargs={"id": "<id>"},
        schema="AuthorSchema",
        type_="author",
        many=False,
    )
    tags = Relationship(
        nested="TagSchema",
        attribute="tags",
        related_view="tag_detail",
        related_view_kwargs={"id": "<id>"},
        schema="TagSchema",
        type_="tag",
        many=True,
    )
