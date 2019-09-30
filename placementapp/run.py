# from flask import Flask, render_template, redirect, flash, url_for,current_app, request
# from forms import User_Registration, User_Information
# from wtforms.validators import ValidationError
# from werkzeug.utils import secure_filename
from PlacementHunters import app


if __name__=='__main__':
    app.run(debug=True)

#export FLASK_APP=app.py
#flask run
#export FLASK_ENV=developer