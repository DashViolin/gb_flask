from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from ..extensions import db
from ..models.user import User

auth_app = Blueprint("auth_app", import_name=__name__, url_prefix="/auth", static_folder="../static")


@auth_app.route("/login/", methods=["GET", "POST"], endpoint="login")
def login():
    if request.method == "GET":
        if not current_user.is_authenticated:
            return render_template("auth/login.html")
        return redirect(url_for("index_app.root"))
    username = request.form.get("username")
    if not username:
        return render_template("auth/login.html", error="username not passed")
    password = request.form.get("password")
    if not password:
        return render_template("auth/login.html", error="password not passed")
    user = User.query.filter_by(username=username).one_or_none()
    if not user:
        return render_template("auth/login.html", error=f"no user {username!r} found")
    if user.password != password:
        return render_template("auth/login.html", error="wrong password!")
    login_user(user)
    user.last_login = datetime.now()
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("index_app.root"))


@auth_app.route("/logout/", endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index_app.root"))


__all__ = [
    "auth_app",
]
