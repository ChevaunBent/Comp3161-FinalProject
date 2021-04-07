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
    servings = IntegerField('Servings', validators=[InputRequired()])
    nutrition_no = IntegerField('Nutrition Number', validators=[InputRequired()])
    calories = IntegerField('Calories', validators=[InputRequired()])
    total_fat = IntegerField('Total Fat', validators=[InputRequired()])
    sugar = IntegerField('Sugar', validators=[InputRequired()])
    sodium = IntegerField('Sodium', validators=[InputRequired()])
    protein = IntegerField('Protein', validators=[InputRequired()])
    saturated_fat = IntegerField('Saturated Fat', validators=[InputRequired()])
    instructions = StringField('Instructions, ', validators=[InputRequired(),Length(min=1, max=400)])
    upload = FileField('Photo', validators=[FileRequired(),FileAllowed(['jpg', 'jpeg', 'png'], 
    'PLease select an Image!')])
    
class NewMeal(FlaskForm):
    name = StringField('Meal Title', validators=[InputRequired(),Length(min=1, max=50)])
    