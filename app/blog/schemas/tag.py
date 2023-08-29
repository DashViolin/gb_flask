from marshmallow_jsonapi import Schema
from marshmallow_jsonapi.fields import Integer, String


class TagSchema(Schema):
    class Meta:
        type_ = "tag"
        self_view = "tag_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "tag_list"

    id = Integer(as_string=True)
    name = String(allow_none=False, required=True)
