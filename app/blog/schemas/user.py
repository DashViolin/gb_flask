from combojsonapi.utils import Relationship
from marshmallow_jsonapi import Schema
from marshmallow_jsonapi.fields import Boolean, Integer, String


class UserSchema(Schema):
    class Meta:
        type_ = "user"
        self_view = "user_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "user_list"

    id = Integer(as_string=True)
    first_name = String(allow_none=False)
    last_name = String(allow_none=False)
    username = String(allow_none=False)
    email = String(allow_none=False)
    is_staff = Boolean(allow_none=False)
    author = Relationship(
        nested="AuthorSchema",
        attribute="author",
        related_view="author_detail",
        related_view_kwargs={"id": "<id>"},
        schema="AuthorSchema",
        type_="author",
        many=False,
    )
