from flask import Flask, render_template, redirect, flash, url_for,current_app, request
from PlacementHunters import app#, db, bcrypt
from PlacementHunters.forms import User_Registration, User_Information, Home_form
from wtforms.validators import ValidationError
from werkzeug.utils import secure_filename
# from PlacementHunters.model import Job_Seekers,Companies
# from flask_login import login_user, current_user, logout_user, login_required


@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/sign',methods=['GET','POST'])
def user_reg():
    if current_user.is_authenticated:#if we already have a user logged in, cant see this registration page
        return redirect(url_for('landingPage'))
    form = User_Registration()
    if form.validate_on_submit():
        # flash(f'Account created for {form.firstname.data}!', 'success')
        # print(form)
        print("registration form valid")
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        seeker = Job_Seekers(aadhar_no=form.aadhar_number.data,username=form.username.data,password=hashed_pwd,email=form.emailid.data)
        db.session.add(seeker)#add user to the database. Later only add after payment.
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('user_info'))#go for further information
    return render_template("user_reg.html", form = form)

@app.route('/info',methods=['GET','POST'])
def user_info():
    form = User_Information()
    # print(form.post_graduation_yes_no)
    for i in form:
        print(i.label, i.data)
    print(request.form.get('blabla'))
    #graduation_marksheet = secure_filename(form.graduation_marksheet.file.filename)
    # if form.graduation_marksheet.file.filename.split('.')[-1] not in ALLOWED_EXTENSIONS:
    #     raise ValidationError("File must be in PDF format")
    #     return render_template("user_info.html", form = form)

    if form.validate_on_submit(): 
        return redirect(url_for('home'))
    else:
        print("bye")
    return render_template("user_info.html", form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('landingPage'))


@app.route('/', methods=['GET', 'POST'])
@app.route('/landingPage', methods=['GET', 'POST'])
def landingPage():
    form = Home_form() #insatnce of form
    print("main route")
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print("valid")
        #if creds exist, log them in
        if form.login.data:#if the user presses the log in button
            seeker = Job_Seekers.query.filter_by(username=form.username.data).first()
            print(seeker)
            if seeker and bcrypt.check_password_hash(seeker.password,form.password.data):
            #check if data in database
                print("here")
                print("Seeker again",seeker)
                login_user(seeker,remember=False)
                print("login succ")
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('Profile'))#tzke the user to the profile page
            elif seeker and not bcrypt.check_password_hash(seeker.password,form.password.data):
                print("invalid password try again ")#make this the flash message thingy
            else:
                #if the seeker dosent exist in the databse 
                return redirect(url_for('user_reg'))
        elif form.register.data:
            print('in elif')
            return redirect(url_for('user_reg'))
        #else go to register page. and then ask what kind of user etc. 
    print("ended here")
    return render_template("landingPage.html", title="Home", form=form)

@app.route('/ProfilePage')
@login_required
def Profile():

    return render_template("profilePage.html")

def recommendation():
    #take job seeker info from current 
@app.route('/JobPage')
def Jobs():
    return render_template("jobBrowsing.html")

@app.route('/contactUs')
def contact():
    return render_template("contact.html")
