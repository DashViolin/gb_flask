from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectMultipleField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CreateArticleForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    summary = StringField("Summary", validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired()])
    tags = SelectMultipleField("Tags", coerce=int)
    publish = BooleanField("Publish immediately")
    submit = SubmitField("Save")
