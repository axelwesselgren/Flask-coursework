from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from wtforms import StringField, PasswordField, BooleanField, SubmitField

forbiden_passwords = ['qwerty', '123', 'password']

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=10)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')])
    check = BooleanField('Remember me')
    submit = SubmitField('Submit')

    def validate_password(self, password):
        if password.data in forbiden_passwords:
            raise ValidationError('Password not secure')