from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

from ..db.data_mock import USERS

users = Blueprint(name="users", import_name=__name__, url_prefix="/users", static_folder="../static ")


@users.route("/", endpoint="list")
def users_list():
    return render_template("users/list.html", users=USERS)


@users.route("/<int:pk>", endpoint="details")
def user_detail(pk: int):
    user_obj = USERS.get(pk)
    if user_obj:
        return render_template("users/detail.html", user=user_obj)
    raise NotFound(f"No such user with id={pk}")
