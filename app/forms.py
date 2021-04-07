from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, Regexp, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class CreateUser(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    age = IntegerField('Age', validators=[InputRequired(), Regexp("^\d+$")])
    height = StringField('Height', validators=[InputRequired()])
    weight = IntegerField('Weight', validators=[InputRequired()])
    '''email = StringField('Email Address', validators=[InputRequired(), Regexp("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$")])
    telephone = StringField('Telephone', validators=[InputRequired(), Regexp("^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$")])
    preference = SelectField(label='Meal Type', choices=[("Gain Weight", "Gain Weight"), ("Lose Weight", "Lose Weight")])
    username = StringField('Username', validators=[InputRequired()])'''
    password = PasswordField('Password', validators=[InputRequired()]) 
    confirm = PasswordField('Retype Password', validators=[InputRequired()])

class UploadForm(FlaskForm):
    ''' title = StringField('Recipe Title', validators=[InputRequired(),Length(min=1, max=50)])
    instructions = TextAreaField('Instructions', validators=[InputRequired(),Length(min=1, max=250)])
    '''
    name = StringField('Recipe Title', validators=[InputRequired(),Length(min=1, max=50)])
    serving = StringField('Serving', validators=[InputRequired(),Length(min=1, max=25)])
    nutrition_no = StringField('Nutrition Number', validators=[InputRequired(),Length(min=1, max=25)])
    calories = StringField('Calories', validators=[InputRequired(),Length(min=1, max=25)])
    total_fat = StringField('Total Fat', validators=[InputRequired(),Length(min=1, max=25)])
    sugar = StringField('Sugar', validators=[InputRequired(),Length(min=1, max=25)])
    sodium = StringField('Sodium', validators=[InputRequired(),Length(min=1, max=25)])
    protein = StringField('Protein', validators=[InputRequired(),Length(min=1, max=25)])
    saturated_fat = StringField('Saturated Fat', validators=[InputRequired(),Length(min=1, max=25)])
    upload = FileField('Photo', validators=[FileRequired(),FileAllowed(['jpg', 'jpeg', 'png'],'Please select an Image!')])

