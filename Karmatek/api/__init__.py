####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from Karmatek import api, app, db, mail
from Karmatek.model import User, Events
from Karmatek.users.views import serializer, Message
from Karmatek.api.credentials_confirm import check_admin_cred, update_admin_cred

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
        if ('user' in request.headers and 'password' in request.headers):
            if (check_admin_cred(request.headers.get('user'), request.headers.get('password'))):
                users = list(User.query.all())
                events = list(Events.query.all())

                return [[user.json() for user in users if (user.confirm)], [event.json() for event in events]]

            else:
                return {'message': 'Access Denied'}, 403
        
        else:
            return {'message': 'Access Denied'}, 403
    
# POST REQUEST: Returns the list of unconfirmed users and re-sends the confirmation mail to them

    def post(self):
        if ('user' in request.headers and 'password' in request.headers):
            if (check_admin_cred(request.headers.get('user'), request.headers.get('password'))):
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

# PUT REQUEST: Updates the admin details (name and/or password)

    def put(self):
        if ('user' in request.headers and 'password' in request.headers):
            if (check_admin_cred(request.headers.get('user'), request.headers.get('password'))):
                if ('user_new' in request.headers or 'password_new' in request.headers):
                    if ('user_new' in request.headers):
                        username = request.headers.get('user_new')
                    else:
                        username = None

                    if ('password_new' in request.headers):
                        password = request.headers.get('password_new')
                    else:
                        password = None

                    update_admin_cred(username, password)
                else:
                    return {'message': 'New details not found'}, 404

            else:
                return {'message': 'Access Denied'}, 403
        
        else:
            return {'message': 'Access Denied'}, 403

# PATCH REQUEST: Checks if the admin details is correct

    def patch(self):
        if ('user' in request.headers and 'password' in request.headers):
            if (check_admin_cred(request.headers.get('user'), request.headers.get('password'))):
                return {"status": "Accepted"}
            
            else:
                return {"status": "Rejected"}, 403
        
        else:
            return {"status": "Rejected"}, 403
            

api.add_resource(Api_endpoint_Resource, '/api')
