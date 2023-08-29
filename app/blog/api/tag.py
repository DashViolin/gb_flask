from flask_combo_jsonapi import ResourceDetail, ResourceList

from ..extensions import db
from ..models import Tag
from ..schemas import TagSchema


class TagList(ResourceList):
    schema = TagSchema
    data_layer = {
        "session": db.session,
        "model": Tag,
    }


class TagDetail(ResourceDetail):
    schema = TagSchema
    data_layer = {
        "session": db.session,
        "model": Tag,
    }
