from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange, Length
from wtforms import RadioField, SubmitField, StringField, IntegerField

class WormForm(FlaskForm):
    name = StringField("Name", validators=[
        DataRequired(),
        Length(min=2, max=15)
    ])
    length = IntegerField("Length", validators=[
        DataRequired(),
        NumberRange(min=0, max=50)
    ])
    submit = SubmitField("Create")

class SortForm(FlaskForm):
    sort = RadioField("Sort Order", choices=[
        ('ASC', 'Ascending'),
        ('DESC', 'Desending')
    ], default='ASC')
    submit = SubmitField("Sort")