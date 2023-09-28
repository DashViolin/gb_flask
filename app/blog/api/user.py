from flask_combo_jsonapi import ResourceDetail, ResourceList

from ..extensions import db
from ..models import User
from ..permissions.user import UserPermission
from ..schemas import UserSchema


class UserList(ResourceList):
    schema = UserSchema
    data_layer = {
        "session": db.session,
        "model": User,
    }


class UserDetail(ResourceDetail):
    schema = UserSchema
    data_layer = {
        "session": db.session,
        "model": User,
        "permission_get": [UserPermission],
    }
