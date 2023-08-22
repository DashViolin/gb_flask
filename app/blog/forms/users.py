from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class UserBaseForm(FlaskForm):
    username = StringField("Username")
    fullname = StringField("Full name")
    email = StringField(
        "E-mail",
        validators=[DataRequired(), Email(), Length(min=5, max=200)],
        filters=[lambda data: data and data.lower()],
    )


class RegistrationForm(UserBaseForm):
    password = PasswordField(
        "New Password",
        validators=[DataRequired(), EqualTo("confirm_password", message="Passwords must match")],
    )
    confirm_password = PasswordField("Repeat Password")
    submit = SubmitField("Register")


class AdminRegistrationForm(RegistrationForm):
    is_staff = BooleanField("Is staff")
