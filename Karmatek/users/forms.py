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
    
    