####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from hashlib import sha256
from pickle import load, dump

####################################################
# GET ADMIN DETAILS (HELPER) #######################
####################################################

def get_admin_cred():
    with open('data.dat', 'rb') as data:
        admin = load(data)

    return admin

####################################################
# UPDATE ADMIN DETAILS (HELPER) ####################
####################################################

def update_admin_cred(username=None, password=None):
    admin = get_admin_cred()
    user = {}

    if (username):
        user['user'] = sha256(username.encode()).hexdigest()
    else:
        user['user'] = admin['user']
    
    if (password):
        user['password'] = sha256(password.encode()).hexdigest()
    else:
        user['password'] = admin['password']
    
    with open('data.dat', 'wb') as data:
        user = dump(admin, data)

####################################################
# VALIDATE ADMIN DETAILS (HELPER) ##################
####################################################

def check_admin_cred(username, password):
    user = {'user': sha256(username.encode()).hexdigest(), 
        'password': sha256(password.encode()).hexdigest()}
    
    admin = get_admin_cred()
    
    if (admin['user'] == user['user'] and admin['password'] == user['password']):
        return True
    else:
        return False