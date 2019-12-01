####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from Karmatek import api
from Karmatek.model import User, Events

####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from flask_restful import Resource
from flask import Blueprint, request, abort

####################################################
# BLUEPRINT SETUP ##################################
####################################################

api_blueprint = Blueprint('api', __name__)

####################################################
# API SETUP ########################################
####################################################

class Api_endpoint_Resource(Resource):
    def get(self):
        if ('user' in request.headers and request.headers.get('user') == 'admin'):
            if ('password' in request.headers and request.headers.get('password') == 'supersecretpassword'):
                users = list(User.query.all())
                events = list(Events.query.all())

                return [[user.json() for user in users if (user.confirm)], [event.json() for event in events]]

            else:
                abort(403)
        
        else:
            return abort(403)

api.add_resource(Api_endpoint_Resource, '/api')
