from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Regexp, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class CreateUser(FlaskForm):
    firstname = StringField('Firstname', validators=[InputRequired()])
    lastname = StringField('Lastname', validators=[InputRequired()])
    age = StringField('Age', validators=[InputRequired(), Regexp("^\d+$")])
    email = StringField('Email Address', validators=[InputRequired(), Regexp("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$")])
    telephone = StringField('Telephone', validators=[InputRequired(), Regexp("^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$")])
    preference = SelectField(label='Meal Type', choices=[("Gain Weight", "Gain Weight"), ("Lose Weight", "Lose Weight")])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm = PasswordField('confirm', validators=[InputRequired()])

class UploadForm(FlaskForm):
    title = StringField('Recipe Title', validators=[InputRequired(),Length(min=1, max=50)])
    instructions = StringField('Instructions', validators=[InputRequired(),Length(min=1, max=250)])
    upload = FileField('Photo', validators=[FileRequired(),FileAllowed(['jpg', 'jpeg', 'png'], 
    'PLease select an Image!')])