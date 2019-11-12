from Karmatek import app

from flask import render_template, Blueprint

core = Blueprint('core', __name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/coordinator')
def coordinator():
    return render_template('coordinator-details.html')

@app.route('/union')
def union():
    return render_template('union-details.html')