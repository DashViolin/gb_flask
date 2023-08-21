from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required
from werkzeug.exceptions import Forbidden, NotFound

from ..models.users import User

users_app = Blueprint(name="users_app", import_name=__name__, url_prefix="/users", static_folder="../static")


@users_app.route("/", endpoint="list")
@login_required
def users_list():
    if current_user.is_staff:
        users = User.query.all()
        return render_template("users/list.html", users=users)
    return redirect(url_for("index_app.root"), code=403)


@users_app.route("/<int:pk>", endpoint="details")
@login_required
def user_detail(pk: int):
    user = User.query.get_or_404(pk)
    if not user:
        raise NotFound(f"No such user with id={pk}")
    if user == current_user or current_user.is_staff:
        return render_template("users/detail.html", user=user)
    return redirect(url_for("index_app.root"), code=403)
