from PlacementHunters import app
from flask import Flask, render_template, redirect, url_for, session, flash
import json
from PlacementHunters.forms import Home_form, Job_Seeker, Seeker_Info
# from PlacementHunters.forms import Job_Seeker, User_Information, Home_form

#for psycopg:
import psycopg2
conn = psycopg2.connect("dbname=JobHunters user=postgres password=kjsce")
cur = conn.cursor()
print("connection successful",conn)

@app.route('/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
def home():
    form = Home_form() #insatnce of form
    print("main route")

    if form.validate_on_submit():
        q1 = f"SELECT password FROM public.\"Job_Seekers\" WHERE username='{form.username.data}'"
        cur.execute(q1)
        pw = cur.fetchone()
        if pw[0] is "null":
            error='Username is incorrect'
            form.username.errors.append(error)
            return render_template("landingPage.html", title="Home",form=form,session=session)
        else:
            if pw[0]==form.password.data:
                session['username']=form.username.data
                form.username.data=""
                form.password.data=""
                #flash(f'You were successfully logged in','success')
                print("LOGGEDIN")
                return render_template("landingPage.html",title="Home",form=form,session=session)
            else:
                error='Password is incorrect'
                form.username.errors.append(error)
                form.password.data=""
                return render_template("landingPage.html", title="Home",form=form,session=session)
    return render_template("landingPage.html", title="Home",form=form,session=session)

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('home'))

# @app.route('/sign',methods=['GET','POST'])
# def user_reg():
#     form = Job_Seeker()
#     if form.validate_on_submit():
#         #the form is valid with method POST
#         x = form.aadhar_number.data
#         print(x)
#         cur.execute(f"INSERT INTO test VALUES('{x}')")
#         conn.commit()
#         return redirect(url_for('user_info'))#go for further information
#     return render_template("user_reg.html", form = form)

def recommendation():
    #take job seeker info from current user logged in 
    aadhar_number = 84512645
    #find the skillset from the seeker_skillset table:
    seeker_skillset = []
    query_str = f"SELECT skill_id FROM seeker_skills WHERE seeker_id = {aadhar_number}"
    cur.execute(query_str)
    skills = cur.fetchall()
    print("skills",skills)
    for skill in skills:
        seeker_skillset.append(skill[0])
    print("seeker skillset is",seeker_skillset)

    #make a dictionary to store the job percentages 
    percent = {}
    query_str = f"SELECT * FROM public.\"Jobs\""#list all the possible jobs present on system
    cur.execute(query_str)
    jobs = cur.fetchall()
    print(jobs)
    for job in jobs:#for each job find the percentage. 
        job_skillset = []
        query_str = f"SELECT skill_id FROM jobs_skills WHERE job_id = {job[0]}"
        cur.execute(query_str)
        skills = cur.fetchall() 
        print("skills in job",skills)
        for skill in skills:
            job_skillset.append(skill[0])
        print("job skillset is",job_skillset,"for job",job[0])
        num = 0
        #calculate percentage:
        for x in job_skillset:
            if x in seeker_skillset:#even seeker has this skill
                num+=1
        percentage = (num/len(job_skillset))*100
        percent[job[0]] = percentage
        print("for job",job[0],"the percentage is",percentage,"And the ditionary is",percent)
    '''
    we can work only on the skil_id and dont eeven need to find the corresponding skill name 
    '''
    #sorting percent based on percentages value:
    percent = sorted(percent.items(), key=lambda x: x[1], reverse=True)
    return percent,jobs


@app.route('/JobPage')
def Jobs():
    percent,jobs = recommendation()
    #percent is list of tuples and 
    #jobs is also list of tuples. 
    return render_template("jobBrowsing.html",percent = json.dumps(percent), jobs = json.dumps(jobs))

@app.route('/allJobsPage')
def all_Jobs():
    query_str = f"SELECT * FROM public.\"Jobs\""#list all the possible jobs present on system
    cur.execute(query_str)
    jobs = cur.fetchall()
    print(jobs)
    return render_template("allJobsPage.html",jobs = json.dumps(jobs))


@app.route('/jsSignUp',methods=['GET','POST'])
def js_signup():
    form = Job_Seeker()
    if form.validate_on_submit():
        q1 = f"SELECT aadhar_number FROM public.\"Job_Seekers\" WHERE username='{form.username.data}'"
        cur.execute(q1)
        user_name = cur.fetchone()
        if json.dumps(user_name) is not "null":
            error='Username already exists'
            form.username.errors.append(error)
            return render_template("user_reg.html",form=form)
        else:
            query_str = f"""INSERT into public.\"Job_Seekers\"(aadhar_number,username,firstname,middlename,
                lastname,address,gender,mobile,emailid,password,dob) VALUES ({form.aadhar_number.data},
                '{form.username.data}','{form.firstname.data}','{form.middlename.data}','{form.lastname.data}',
                '{form.address.data}','{form.gender.data}',{form.mobile.data},'{form.emailid.data}','{form.password.data}','{form.dob.data}')"""
            try:
                cur.execute(query_str)
                conn.commit()
                session['username']=form.username.data
                # print(session['username'])
                return redirect(url_for('js_info'))
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)          
    return render_template("user_reg.html",form=form)

def getSession():
    if 'username' in session:
        return session['username']
    return 0

@app.route('/Info',methods=['GET','POST'])
def js_info():
    form = Seeker_Info()
    js_username = getSession()
    print(js_username)
    if form.validate_on_submit():
        js_username = getSession()
        print("hi")
        print(js_username)
        query_str = f"""UPDATE public.\"Job_Seekers\" SET school_name='{form.school_name.data}',
            tenth_percent='{form.tenth_percent.data}',junior_college_name='{form.junior_college_name.data}',
            twelfth_percent='{form.twelfth_percent.data}',graduation_college_name='{form.graduation_college_name.data}',
            graduation_cgpa='{form.graduation_cgpa.data}',graduation_course_name='{form.graduation_course_name.data}',
            graduation_year_of_passing='{form.graduation_year_of_passing.data}',
            about_yourself='{form.about_yourself.data}',hobbies='{form.hobbies.data}'  WHERE username='{js_username}'"""
        
        try:
            cur.execute(query_str)
            conn.commit()
            # print(session['username'])
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            return render_template('user_info.html',form=form)

        if form.post_graduation_yes_no.data=='Y':
            print('heree')
            query_str = f"""UPDATE public.\"Job_Seekers\" SET graduation_college_name='{form.post_graduation_college_name.data}',
            post_graduation_cgpa='{form.post_graduation_cgpa.data}',post_graduation_course_name='{form.post_graduation_course_name.data}',
            post_graduation_year_of_passing='{form.post_graduation_year_of_passing.data}' WHERE username='{js_username}'"""
 
            try:
                cur.execute(query_str)
                conn.commit()
                print("exectuted!")
                # print(session['username'])
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                return render_template('user_info.html',form=form)
        return redirect(url_for('home'))
    print(form.errors)
    return render_template('user_info.html',form=form)