# from flask import Flask, render_template, redirect, flash, url_for,current_app, request
# from forms import User_Registration, User_Information
# from wtforms.validators import ValidationError
# from werkzeug.utils import secure_filename
# from flask_sqlalchemy import SQLAlchemy

# ALLOWED_EXTENSIONS = ['pdf']
# app=Flask(__name__)
# app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


# @app.route('/')
# @app.route('/home')
# def home():
#     return render_template("home.html")

# @app.route('/reg_seeker',methods=['GET','POST'])
# def user_reg():
#     form = User_Registration()
#     if form.validate_on_submit():
#         # flash(f'Account created for {form.firstname.data}!', 'success')
#         # print(form)
#         return redirect(url_for('user_info'))
#     return render_template("user_reg.html", form = form)

# @app.route('/info',methods=['GET','POST'])
# def user_info():
#     form = User_Information()
#     # print(form.post_graduation_yes_no)
#     for i in form:
#         print(i.label, i.data)
#     print(request.form.get('blabla'))
#     #graduation_marksheet = secure_filename(form.graduation_marksheet.file.filename)
#     # if form.graduation_marksheet.file.filename.split('.')[-1] not in ALLOWED_EXTENSIONS:
#     #     raise ValidationError("File must be in PDF format")
#     #     return render_template("user_info.html", form = form)

#     if form.validate_on_submit(): 
#         return redirect(url_for('home'))
#     else:
#         print("bye")
#     return render_template("user_info.html", form = form)

# if __name__=='__main__':
#     app.run(debug=True)

# #export FLASK_APP=app.py
# #flask run
# #export FLASK_ENV=developer