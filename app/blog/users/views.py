from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

from ..db.data_mock import USERS

user = Blueprint(name="user", import_name=__name__, url_prefix="/users", static_folder="../static ")


@user.route("/")
def users_list():
    return render_template("users/list.html", users=USERS, active_page="users")


@user.route("/<int:pk>")
def user_detail(pk: int):
    user_obj = USERS.get(pk)
    if user_obj:
        return render_template("users/detail.html", user=user_obj, active_page="users")
    raise NotFound
