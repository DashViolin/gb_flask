from flask_combo_jsonapi import ResourceDetail, ResourceList

from ..extensions import db
from ..models import Author
from ..schemas import AuthorSchema


class AuthorList(ResourceList):
    schema = AuthorSchema
    data_layer = {
        "session": db.session,
        "model": Author,
    }


class AuthorDetail(ResourceDetail):
    schema = AuthorSchema
    data_layer = {
        "session": db.session,
        "model": Author,
    }
