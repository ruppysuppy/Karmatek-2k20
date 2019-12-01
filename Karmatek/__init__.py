####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from datetime import timedelta
from flask import Flask, render_template, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_login import LoginManager
import os

####################################################
# APP SETUP ########################################
####################################################

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret_key'

####################################################
# DATABASE SETUP ###################################
####################################################

base_dir = os.path.abspath(os.path.dirname(__name__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

####################################################
# COOKIE LIFETIME SETUP ############################
####################################################

app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)

####################################################
# EMAIL SETUP ######################################
####################################################

app.config.update(
	DEBUG = False,
	#EMAIL SETTINGS
	MAIL_SERVER = 'smtp.gmail.com',
	MAIL_PORT = 465,
	MAIL_USE_SSL = True,
	MAIL_USERNAME = "youremailid(if its not from gmail, change the mail server)",
	MAIL_PASSWORD = "yourpassword"
	)

mail = Mail(app)

####################################################
# MIGRATION SETUP ##################################
####################################################

Migrate(app, db)

####################################################
# API SETUP ########################################
####################################################

api = Api(app)

####################################################
# LOGIN SETUP ######################################
####################################################

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

####################################################
# BLUEPRINT SETUP ##################################
####################################################

from Karmatek.core.views import core
from Karmatek.users.views import users
from Karmatek.error_pages.handler import error_pages
from Karmatek.api import api_blueprint

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error_pages)
app.register_blueprint(api_blueprint)