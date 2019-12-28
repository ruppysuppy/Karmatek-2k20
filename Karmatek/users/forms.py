####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

# Imports for forms

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

# Imports for users

from flask_login import current_user

####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from Karmatek.model import User

####################################################
# LOGIN FORM SETUP #################################
####################################################

class LoginForm(FlaskForm):
    email = StringField('Email'.upper(), validators=[DataRequired(), Email()])
    password = PasswordField('Password'.upper(), validators=[DataRequired()])
    submit = SubmitField('Log In')

####################################################
# REGISTER FORM SETUP ##############################
####################################################

class Register(FlaskForm):
    email = StringField('Email'.upper(), validators=[DataRequired(), Email()])
    name = StringField('Full Name'.upper(), validators=[DataRequired()])
    password = PasswordField('Password'.upper(), validators=[DataRequired()])
    pass_confirm = PasswordField('Confirm Password'.upper(), validators=[DataRequired(), EqualTo('password', 'Both the Password Fields Must Match')])
    ph_num = IntegerField("Phone Number".upper(), validators=[DataRequired()])
    dept = StringField("Department".upper(), validators=[DataRequired()])
    year = IntegerField("Academic Year".upper(), validators=[DataRequired()])
    submit = SubmitField('REGISTER')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The email entered has already been registered')

####################################################
# UPDATION SETUP ###################################
####################################################

class UpdateUserForm(FlaskForm):
    email = StringField('Email'.upper(), validators=[DataRequired(), Email()])
    name = StringField('Name'.upper(), validators=[DataRequired()])
    ph_num = IntegerField("Phone Number".upper(), validators=[DataRequired()])
    dept = StringField("Department".upper(), validators=[DataRequired()])
    year = IntegerField("Academic Year".upper(), validators=[DataRequired()])
    submit = SubmitField('UPDATE')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The email entered has already been registered')

####################################################
# EVENT SELECTION SETUP ############################
####################################################    

class EventsForm(FlaskForm):
    event_selector = SelectField("Select Events to Participate in".upper(), choices=[
        ("Robo Race", "Robo Race"),
        ("Robo Carrom", "Robo Carrom"),
        ("Robo Soccer", "Robo Soccer"),
        ("Robo Maze", "Robo Maze"),
        ("Autonomous Line Follower", "Autonomous Line Follower"),
        ("Code Beta", "Code Beta"),
        ("Code Pro", "Code Pro"),
        ("Web Designing", "Web Designing"),
        ("Pubg", "Pubg"),
        ("NFS Most Wanted", "NFS Most Wanted"),
        ("Fifa", "Fifa"),
        ("Call of Duty", "Call of Duty"),
        ("Chess", "Chess"),
        ("Nail it @19", "Nail it @19"),
        ("Petapixel", "Petapixel"),
        ("Memester Challenge", "Memester Challenge"),
        ("Matrivia", "Matrivia"),
        ("Fandom", "Fandom"),
        ("Ek Duje ke liye", "Ek Duje ke liye"),
        ("CubicMatics", "CubicMatics")
    ])
    submit = SubmitField('ADD')