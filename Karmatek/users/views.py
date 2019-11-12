####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_user, logout_user, current_user, login_required

####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from Karmatek.users.forms import LoginForm, Register
from Karmatek.model import User
from Karmatek import login_manager, db

####################################################
# BLUEPRINT SETUP ##################################
####################################################

users = Blueprint('users', __name__)

####################################################
# LOGIN SETUP ######################################
####################################################

@users.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if (user is not None and user.check_password(form.password.data)):
            login_user(user)
            flash('Login Successful!')

            next = request.args.get('next')

            if (next == None or not next[0] == '/'):
                next = url_for('home')
            
            return redirect(next)
        
        else:
            flash('Incorrect Username/Password!')
    
    return render_template('login.html', form=form)

####################################################
# REGISTRATION SETUP ###############################
####################################################

@users.route('/register', methods=["GET", "POST"])
def register():
    form = Register()

    if form.validate_on_submit():
        user1 = User.query.filter_by(email=form.email.data).first()

        if (user1 == None):
            user = User(email=form.email.data, username=form.name.data, password=form.password.data, ph_num=form.ph_num.data, dept=form.dept.data, year=form.year.data)
            db.session.add(user)
            db.session.commit()

            flash('Thankyou for Registering. Welcome to Karmatek 2k20!')

            return redirect(url_for('users.login'))
        
        else:
            flash('Email already registered')
    
    return render_template('register.html', form=form, page_name="Registration")

####################################################
# LOGOUT SETUP #####################################
####################################################

@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully Logged Out!')
    return redirect(url_for('home'))