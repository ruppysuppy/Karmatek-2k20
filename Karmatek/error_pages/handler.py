####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from flask import Blueprint, render_template

####################################################
# BLUEPRINT SETUP ##################################
####################################################

error_pages = Blueprint('error_pages', __name__)

####################################################
# ERROR 404 SETUP ##################################
####################################################

@error_pages.app_errorhandler(404)
def error_404(error):
    return render_template('error_pages/404.html', page_name="404 Error"), 404

####################################################
# ERROR 403 SETUP ##################################
####################################################

@error_pages.app_errorhandler(403)
def error_403(error):
    return render_template('error_pages/403.html', page_name="403 Error"), 403

####################################################
# ERROR 500 SETUP ##################################
####################################################

@error_pages.app_errorhandler(500)
def error_500(error):
    return render_template('error_pages/500.html', page_name="500 Error"), 500