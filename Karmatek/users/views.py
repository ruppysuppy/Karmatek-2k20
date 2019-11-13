####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_user, logout_user, current_user, login_required

####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from Karmatek.users.forms import LoginForm, Register, UpdateUserForm, EventsForm
from Karmatek.model import User, Events
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
            flash('Email already registered!')
    
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

####################################################
# PROFILE SETUP ####################################
####################################################

@users.route('/account', methods=["GET", "POST"])
@login_required
def account():
    form = UpdateUserForm()
    form.email.data = current_user.email
    events = list(Events.query.filter_by(user_id=current_user.id))
    events_form = EventsForm()

    if events_form.validate_on_submit():
        temp = Events(current_user.id, events_form.event_selector.data)
        db.session.add(temp)
        db.session.commit()

        return redirect(url_for('users.account'))
    
    if form.validate_on_submit():
        current_user.username = form.name.data
        current_user.ph_num = form.ph_num.data
        current_user.dept = form.dept.data
        current_user.year = form.year.data

        db.session.commit()

        flash('User Account Updated!')

        return redirect(url_for('home'))

    elif request.method == "GET":
        form.name.data = current_user.username
        form.ph_num.data = current_user.ph_num
        form.dept.data = current_user.dept
        form.year.data = current_user.year

    return render_template('profile.html', form=form, events_form=events_form, events=events)
