from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CreateArticleForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    summary = StringField("Title", validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired()])
    publish = BooleanField("Publish immediately")
    submit = SubmitField("Save")
