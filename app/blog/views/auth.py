from datetime import datetime

from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..forms.users import LoginForm, RegistrationForm
from ..models.users import User

auth_app = Blueprint("auth_app", import_name=__name__, url_prefix="/auth", static_folder="../static")


@auth_app.route("/login/", methods=["GET", "POST"], endpoint="login")
def login():
    errors = []
    form = LoginForm(request.form)
    if request.method == "GET":
        if not current_user.is_authenticated:
            return render_template("auth/login.html", form=form, errors=errors)
        return redirect(url_for("index_app.root"))
    if form.validate_on_submit():
        if not form.username.data:
            errors.append("Username not passed")
        if not form.password.data:
            errors.append("Password not passed")
        user = User.query.filter_by(username=form.username.data).one_or_none()
        if user and user.validate_password(form.password.data):
            login_user(user)
            user.last_login = datetime.now()
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("index_app.root"))
        else:
            errors.append("Wrong credentials")
    return render_template("auth/login.html", form=form, errors=errors)


@auth_app.route("/logout/", endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index_app.root"))


@auth_app.route("/register/", endpoint="register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index_app.root"))
    errors = []
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).count():
            form.username.errors.append("username already exists!")
            return render_template("auth/register.html", form=form, errors=errors)
        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append("email already exists!")
            return render_template("auth/register.html", form=form, errors=errors)
        user_data = {
            "username": form.username.data,
            "fullname": form.fullname.data,
            "email": form.email.data,
            "password": form.password.data,
        }
        user = User(**user_data)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            msg = "Could not create user!"
            current_app.logger.exception(msg)
            errors.append(msg)
        else:
            current_app.logger.info("Created user %s", user)
            login_user(user)
        return redirect(url_for("index_app.root"))
    return render_template("auth/register.html", form=form, errors=errors)


__all__ = [
    "auth_app",
]
