# Karmatek-2k20
This is the website for Karmatek 2k20, the tech fest of Govenment College of Engineering and Ceramic Technology.

## Languages/Frameworks/Techlogy Used
This project uses the following technologies:
* Python 3.x
* Flask 1.11
* Flask-Login 0.41
* WTForms 2.2.1
* Werkzeug 0.16.0
* HTML 5
* CSS 3

### Note
The front-end was made by Rajashi Chaterjee using the template "The Event" available at BootstrapMade (https://bootstrapmade.com/)

## How to use (for non-technical people/beginners)
Follow the steps to the local server on your machine:
* Download and install Python 3.x
* Download the repository
* Extract the repository at the desired location
* Navigate to the extrated folder
* Open the Terminal/CMD/PowerShell at the location (Shift + Right Click => Run Command Prompt for Windows Users)
* Run the Command 'pip install -r requirements.txt' (to install the dependencies)
* Run the Command 'flask db init'
* Run the Command 'flask db migrate -m "< Any message you want to save >"'
* Run the Command 'flask db upgrade'
* If you have problem running the above mentioned commands ('flask db init' onwards), you can uncomment 'db.create_all()' (Line 12) in app.py
* Run the Command 'python app.py'
* Run the website (Navigate to '127.0.0.1:5000' on a web-browser)

### Note
To use the email confirmation, the email id and password has to be entered in Karmatek-2k20/Karmatek/__init__.py ('MAIL_USERNAME' and 'MAIL_PASSWORD' in the 'EMAIL SETUP' Section) and in google settings, less secure app access must be turned on.
To use the site without running into email confirmation issues, in Karmatek-2k20/Karmatek/templates/profile.html, in line 83, replace 'current_user.confirm' with 'True' and comment out line 77 to 107 in Karmatek-2k20/Karmatek/users/views.py