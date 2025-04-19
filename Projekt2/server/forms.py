from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField, IntegerField
from wtforms.validators import DataRequired

class FilterForm(FlaskForm):
    search = StringField("Search")
    submit = SubmitField("Filter")
    
class UpdateEmployeeForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    telephone = StringField("Telephone", validators=[DataRequired()])
    salary = IntegerField("Salary" , validators=[DataRequired()])
    boss = SelectField("Boss", validators=[DataRequired()], choices=[])
    department = SelectField("Department", validators=[DataRequired()], choices=[])
    update = SubmitField("Update")
    
class UpdateDepartmentForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    update = SubmitField("Update")

class AddEmployeeForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    telephone = StringField("Telephone", validators=[DataRequired()])
    salary = IntegerField("Salary" , validators=[DataRequired()])
    boss = SelectField("Boss", validators=[DataRequired()])
    department = SelectField("Department", validators=[DataRequired()])
    add = SubmitField("Add")
    
class AddDepartmentForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    id = StringField("ID", validators=[DataRequired()])
    add = SubmitField("Add")