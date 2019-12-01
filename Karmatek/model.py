####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from Karmatek import db, login_manager

####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user

####################################################
# USER LOADER SETUP ################################
####################################################

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

####################################################
# USER MODEL SETUP #################################
####################################################

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(64))
    ph_num = db.Column(db.String(10))
    dept = db.Column(db.String(128))
    year = db.Column(db.Integer)
    confirm = db.Column(db.Integer, unique=False, default=0)

    posts = db.relationship('Events', backref='author', lazy=True)

    def __init__(self, email, username, password, ph_num, dept, year):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.year = year
        self.dept = dept
        self.ph_num = ph_num
        self.confirm = 0
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User-name: {self.username}\nEmail: {self.email}"
    
    def json(self):
        return {
            'Id': self.id,
            'Name': self.username,
            'Email': self.email,
            'Phone': self.ph_num,
            'Year': self.year,
            'Dept': self.dept,
            'Confirm': self.confirm
            }

####################################################
# PARTICIPATING EVENTs SETUP #######################
####################################################

class Events(db.Model):
    __tablename__ = 'events'

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event = db.Column(db.String(256), nullable=False)

    def __init__(self, user_id, event):
        self.user_id = user_id
        self.event = event
    
    def __repr__(self):
        return f"Event: {self.event}"
    
    def __str__(self):
        return self.__repr__()
    
    def json(self):
        return {
            'Id': self.user_id,
            'Event': self.event
            }