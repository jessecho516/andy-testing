from wtforms.validators import DataRequired
from wtforms import SubmitField, StringField
from flask_wtf import FlaskForm


class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")