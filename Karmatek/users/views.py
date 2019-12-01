####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from flask import Blueprint, render_template, flash, redirect, request, url_for, abort
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from Karmatek.users.forms import LoginForm, Register, UpdateUserForm, EventsForm
from Karmatek.model import User, Events
from Karmatek import app, db, login_manager, mail

####################################################
# BLUEPRINT SETUP ##################################
####################################################

users = Blueprint('users', __name__)

####################################################
# TIMED SERIALIZER SETUP ###########################
####################################################

serializer = URLSafeTimedSerializer('somesecretkey')

####################################################
# LOGIN SETUP ######################################
####################################################

@users.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if (user is not None and user.check_password(form.password.data)):
            login_user(user, remember=True)
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
            if (len(form.password.data) < 6):
                flash('Use a stronger password')
                return redirect(url_for('users.register'))

            user = User(email=form.email.data, username=form.name.data, password=form.password.data, ph_num=form.ph_num.data, dept=form.dept.data, year=form.year.data)
            db.session.add(user)
            db.session.commit()

            token = serializer.dumps(form.email.data, salt='email-confirm')
            link = url_for('users.confirm_email', token=token, _external=True)
            link_home = url_for('home', _external=True)

            msg = Message('Karmatek 2k20 Confirmation', sender=app.config["MAIL_USERNAME"], recipients=[form.email.data])

            msg.body = f'''
\tHello {form.name.data}

Thankyou for registering at Karmatek 2k20. Please click on the link below to confirm your email id.
Your confirmation link is: {link}
Please login to your account and select the events you want to paricipate in as soon as possible at the official Karmatek 2k20 site ({link_home}).
Hope you have an awesome time.
LET'S TECHNICATE....
        
\tYour Sincerely
\tTapajyoti Bose
\tTechincal Head
\tKarmatek 2k20
\tGCECT Tech-fest
            '''

            mail.send(msg)

            flash(f'Thankyou for Registering. Welcome to Karmatek 2k20! A confirmation email has been sent to "{form.email.data}"')

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

    for i in range(len(events)):
        events[i] = (url_for('users.delete', event_id=events[i].id), events[i])
    
    if events_form.validate_on_submit():
        check = list(Events.query.filter_by(user_id=current_user.id, event=events_form.event_selector.data))

        if (check):
            flash("You have already registered for this event!")
        else:
            temp = Events(current_user.id, events_form.event_selector.data)
            db.session.add(temp)
            db.session.commit()
            flash("Registration Successful!")

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

    return render_template('profile.html', form=form, events_form=events_form, events=events, len=len)

####################################################
# EVENT DETAILS SETUP ##############################
####################################################

data_dict = dict([("Robo Race", {'text': 'Design your own robo and bring it on the track to test its power and efficiency. Let’s see who wins the wheel-to-wheel action in this enthralling event.',
            'd&t': '10/03/2020 12:30pm'}),
        ("Robo Carrom", {'text' : 'Bring your robot to test its skills and agility. Register today and see how good your bot is at playing carrom.',
            'd&t' : '10/03/2020 03:30pm'}),
        ("Robo Soccer", {'text' : 'Because the robo is not just speed. Yes, your droid/ robot can do a lot more. Let your robot kick the ball while you get the prize money if it wins.',
            'd&t' : '10/03/2020 06:30pm'}),
        ("Robo Maze", {'text' : 'Feel the thrill, feel the tension as your hand made robot moves through a complicated maze. Let’s see who is the fastest to move through the labyrinth!',
            'd&t' : '11/03/2020 12:30pm'}),
        ("Autonomous Line Follower", {'text' : 'Does your droid have the caliber to be the fastest line follower? Build your own autonomous robot and beat others on the track to win an exciting prize money!',
            'd&t' : '11/03/2020 03:30pm'}),
        ("Code Beta", {'text' : 'New to coding? No worries! Hone your coding skills and kick start your CP journey with a challenge meant for beginners. Are you up for it?',
            'd&t' : '10/03/2020 12:30pm'}),
        ("Code Pro", {'text' : 'Put your coding skills to test as you work your way through algorithms like a “PRO”! Grab the title of Code Pro Champ and take home an exciting prize money.',
            'd&t' : '11/03/2020 12:30pm'}),
        ("Web Designing", {'text' : 'Got a talent for web designing? Don’t let it loiter around. Pick a partner and compete with other talented web designers. Test your skills and maybe win to grab the prize money!',
            'd&t' : '10/03/2020 04:30pm'}),
        ("Pubg", {'text' : 'The battleground is all set.\nAssemble your players and fight to remain the last one alive and win not just a chicken dinner but also the prize money.',
            'd&t' : '11/03/2020 02:30pm'}),
        ("NFS Most Wanted", {'text' : 'Everything under control? Then you aren’t moving fast enough.\nGet inside the racing car and race your way to win. Let’s see who wins the race to grab the prize.',
            'd&t' : '11/03/2020 04:30pm'}),
        ("Fifa", {'text' : 'Bring out the e-footballer and the champion within you.\nPut your FIFA skills to test and battle it out to win and take home the prize. So, are you game?',
            'd&t' : '11/03/2020 06:00pm'}),
        ("Call of Duty", {'text' : 'Nothing brings gamers together like a bit of competition. How can a gamer miss a competition of COD? Shoot it like your life depends on it and win an assured prize money.',
            'd&t' : '10/03/2020 04:00pm'}),
        ("Chess", {'text' : '“All that matters on the chessboard is good moves.”- Bobby Fischer\nDo you think you are smart enough to play the winning move? If you have a passion for chess then come and show us how smart you are.',
            'd&t' : '10/03/2020 01:00pm'}),
        ("Nail it @19", {'text' : '“Sometimes, less is more.”- Shakespeare.\nAre you a minimalist with a head full of creativity? Can you knit a crisp and concise write-up with just 19 words? Yes? Come one, come all!',
            'd&t' : '12/03/2020 12:30pm'}),
        ("Petapixel", {'text' : 'Got a knack for photography? Here is an opportunity for all the budding photographers to show off their skills and win a prize.',
            'd&t' : '12/03/2020 02:00pm'}),
        ("Memester Challenge", {'text' : 'Can you just not pass a day without fooling around? If you think that are humorous enough to be a meme maker, then this is your challenge.',
            'd&t' : '12/03/2020 01:30pm'}),
        ("Matrivia", {'text' : 'Do you have a love for material sciences? Here is the fun-filled quiz on material sciences. Use your knowledge and your wit to crack this questionnaire. Are you smart enough?',
            'd&t' : '12/03/2020 12:30pm'}),
        ("Fandom", {'text' : 'Are you a Potterhead? Or a die-hard fan of MCU? Do you know everything about GOT? Put your knowledge to the ultimate test and win the prize.',
            'd&t' : '12/03/2020 01:00pm'}),
        ("Ek Duje ke liye", {'text' : 'Cutest couple in college? Are you the inseparable pair? Hone your way through exciting and fun rounds to show the world what you can do “ek duje ke liye”.',
            'd&t' : '12/03/2020 03:00pm'}),
        ("CubicMatics", {'text' : 'Can you solve the Rubik’s cube within seconds? Then register now to compete with other such speedcubers and win.',
            'd&t' : '12/03/2020 04:30pm'})])

@users.route('/paticipation/<int:event_id>')
def event_detail(event_id):
    event = Events.query.get_or_404(event_id)
    
    try:
        if (event.user_id != current_user.id):
            abort(403)
    except:
        abort(403)
    
    return render_template('event.html', event=event, data_dict=data_dict)

####################################################
# REMOVE PATICIPATION SETUP ########################
####################################################

@users.route('/<int:event_id>/delete', methods=["GET", "POST"])
@login_required
def delete(event_id):
    event = Events.query.get_or_404(event_id)

    try:
        if (event.user_id != current_user.id):
            abort(403)
    except:
        abort(403)
    
    db.session.delete(event)
    db.session.commit()

    flash('Successfully Removed Event Participation!')

    return redirect(url_for('users.account', event=event))

####################################################
# EMAIL CONFIRMATION SETUP #########################
####################################################

@users.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=86400)
        user = User.query.filter_by(email=email).first()
        user.confirm = 1
        db.session.commit()

    except SignatureExpired:
        flash('Signature has expired. Create a new account and confirm the mail as soon as possible.')
        return render_template('home')
    
    flash('Email id Confirmed! Now you can select events to paticiapte in.')
    return redirect(url_for('users.account'))