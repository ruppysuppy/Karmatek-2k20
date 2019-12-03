####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from Karmatek import api, app, db, mail
from Karmatek.model import User, Events
from Karmatek.users.views import serializer, Message

####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from flask_restful import Resource
from flask import Blueprint, request, abort, url_for

####################################################
# BLUEPRINT SETUP ##################################
####################################################

api_blueprint = Blueprint('api', __name__)

####################################################
# API SETUP ########################################
####################################################

class Api_endpoint_Resource(Resource):

# GET REQUEST: Returns the Users who have confirmed the email and the list of events they are paticipating in

    def get(self):
        if ('user' in request.headers and request.headers.get('user') == 'admin'):
            if ('password' in request.headers and request.headers.get('password') == 'supersecretpassword'):
                users = list(User.query.all())
                events = list(Events.query.all())

                return [[user.json() for user in users if (user.confirm)], [event.json() for event in events]]

            else:
                return {'message': 'Access Denied'}, 403
        
        else:
            return {'message': 'Access Denied'}, 403
    
# POST REQUEST: Returns the list of unconfirmed users and re-sends the confirmation mail to them

    def post(self):
        if ('user' in request.headers and request.headers.get('user') == 'admin'):
            if ('password' in request.headers and request.headers.get('password') == 'supersecretpassword'):
                emails = list(db.engine.execute('select users.email \
                    from users \
                    where users.confirm=0'))
                
                for i in range(len(emails)):
                    emails[i] = emails[i][0]
                
                try:
                    for email in emails:
                        token = serializer.dumps(email, salt='email-confirm')
                        link = url_for('users.confirm_email', token=token, _external=True)
                        link_home = url_for('home', _external=True)

                        username = list(db.engine.execute(f'select users.username \
                            from users \
                            where users.email="{email}"'))[0][0]

                        msg = Message('Karmatek 2k20 Confirmation', sender=app.config["MAIL_USERNAME"], recipients=[email])

                        msg.body = f'''
\tHello {username}

Thankyou for registering at Karmatek 2k20. Please click on the link below to confirm your email id.
Your confirmation link is: {link}
Please login to your account and select the events you want to paricipate in as soon as possible at the official Karmatek 2k20 site ({link_home}).
Hope you have an awesome time.
LET'S TECHNICATE....

PS: Ignore the mail if you have already confirmed your mail id.
        
\tYour Sincerely
\tTapajyoti Bose
\tTechincal Head
\tKarmatek 2k20
\tGCECT Tech-fest
            '''

                        mail.send(msg)

                except:
                    print('\nUnable to send mails, please check the user id and password (in Karmatek/__init__.py)\n')
                    return {'message': 'Internal Server Error'}, 500

                return emails
            
            else:
                return {'message': 'Access Denied'}, 403
        
        else:
            return {'message': 'Access Denied'}, 403

api.add_resource(Api_endpoint_Resource, '/api')
