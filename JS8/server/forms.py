from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    login = SubmitField("Login")
    
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    password_repeat = StringField("Repeat Password", validators=[
        DataRequired(),
        EqualTo("password")
    ])
    register = SubmitField("Register")
    
class CreateThreadForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()])
    create = SubmitField("Create Thread")