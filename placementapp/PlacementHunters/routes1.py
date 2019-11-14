from PlacementHunters import app
from flask import Flask, render_template, redirect, url_for, session, flash, request
import json
from PlacementHunters.forms import Home_form, Job_Seeker, Seeker_Info, add_jobs_form,Company_reg
# from PlacementHunters.forms import Job_Seeker, User_Information, Home_form

#for psycopg:
import psycopg2
conn = psycopg2.connect("dbname=JobHunters2 user=postgres password=kjsce")
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
    js_username=getSession()
    query_str = f"SELECT * FROM public.\"Jobs\""#list all the possible jobs present on system
    cur.execute(query_str)
    jobs = cur.fetchall()
    if js_username!=0:
        q1 = f"SELECT aadhar_number from public.\"Job_Seekers\" where username='{js_username}'"
        cur.execute(q1)   
        aadhar_number = cur.fetchone()[0]
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
            query_str = f"SELECT skill_id FROM jobs_skills WHERE job_id = {job[5]}"
            cur.execute(query_str)
            skills = cur.fetchall() 
            print("skills in job",skills)
            for skill in skills:
                job_skillset.append(skill[0])
            print("job skillset is",job_skillset,"for job",job[5])
            num = 0
            #calculate percentage:
            for x in job_skillset:
                if x in seeker_skillset:#even seeker has this skill
                    num+=1
            percentage = (num/len(job_skillset))*100
            percent[job[5]] = percentage
            print("for job",job[0],"the percentage is",percentage,"And the ditionary is",percent)
        '''
        we can work only on the skil_id and dont eeven need to find the corresponding skill name 
        '''
        #sorting percent based on percentages value:
        percent = sorted(percent.items(), key=lambda x: x[1], reverse=True)
        return percent,jobs
    return [],jobs


@app.route('/JobPage')
def Jobs():
    percent,jobs = recommendation()
    print(percent)
    print(jobs)
    #percent is list of tuples and 
    #jobs is also list of tuples. 
    return render_template("jobBrowsing.html",percent = json.dumps(percent), jobs = json.dumps(jobs))

@app.route('/CompanyReg',methods=['GET','POST'])
def Company_registration():
    form = Company_reg()
    if form.validate_on_submit():
        print("company form valid")
        try:#**
            query_str = f"INSERT INTO public.\"Comapny\"(\"GSTIN\",name, username, mobile, address, password, website) VALUES ({int(form.GSTIN.data)}, '{form.name.data}', '{form.username.data}', '{form.mobile.data}', '{form.address.data}',' {form.password.data}', '{form.website.data}')"
            cur.execute(query_str)
            conn.commit()
            count = cur.rowcount
            print (count, "Record inserted successfully into company table")
        except (Exception, psycopg2.Error) as error :
            if(conn):
                print("Failed to insert record into company table", error)
        return redirect(url_for('comapy_profile'))#go for further information
    return render_template("company_reg.html",form = form)


@app.route('/allJobsPage')
def all_Jobs():
    query_str = f"SELECT * FROM public.\"Jobs\""#list all the possible jobs present on system
    cur.execute(query_str)
    jobs = cur.fetchall()
    print(jobs)
    return render_template("allJobsPage.html")

   

@app.route('/CompanyProfile',methods=['GET','POST'])
def company_profile():
    #get company id from the table or session variable. 
    # comapny_username = getSession()#** change
    comapny_username = 'info_ker'
    query_str = f"SELECT \"GSTIN\" FROM public.\"Comapny\" WHERE username = '{comapny_username}';"
    cur.execute(query_str)
    GSTIN = cur.fetchone()[0]
    print(GSTIN)

    query_str = f"SELECT * FROM public.\"Jobs\" WHERE comapany_id = '{GSTIN}';"
    cur.execute(query_str)
    jobs = cur.fetchall()

    query_str = f"SELECT * FROM public.\"Comapny\" WHERE \"GSTIN\" = {GSTIN};"
    cur.execute(query_str)
    company = cur.fetchone()#returns a tuple.

    print("comapyfetch",company)
    print("Job fetch",jobs)
    # data = request.get_json()
    # print(data)
    # print(type(data))
    return render_template("CompanyProfile.html",company= company, jobs = json.dumps(jobs))
    #return render_template("allJobsPage.html",jobs = json.dumps(jobs))


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

    query_str = f"SELECT name FROM skills"
    cur.execute(query_str)
    skills = cur.fetchall()
    print(type(skills[0]))
    skills = [item for t in skills for item in t]
    print("skills",skills)

    print(request.form.getlist('sel'))
    js_username = getSession()
    print(js_username)
    if form.validate_on_submit():
        js_username = getSession()
        print("hi")
        print(js_username)
        skil = request.form.getlist('sel')
        q1 = f"SELECT aadhar_number from public.\"Job_Seekers\" where username='{js_username}'"
        cur.execute(q1)   
        an = cur.fetchone() 
        print(json.dumps(an))
        for s in skills:
            for j in skil:
                if s==j:
                    q2 = f"SELECT skill_id from skills where name='{j}'"
                    cur.execute(q2)
                    a = cur.fetchone()
                    q3 = f"INSERT INTO public.\"seeker_skills\" values({an[0]},{a[0]})"
                    cur.execute(q3)
                    conn.commit()


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
            return render_template('user_info.html',form=form,skills=skills)

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
                return render_template('user_info.html',form=form,skills=skills)
        return redirect(url_for('home'))
    print(form.errors)
    return render_template('user_info.html',form=form)



@app.route('/AddJob',methods=['GET','POST'])
def add_jobs():
    print("here again")
    form = add_jobs_form()
    if form.validate_on_submit():
        print("add jobs form valid")
        print("here")
        try:
            # comapny_username = getSession() #gets username of company
            comapny_username = 'info_ker'#**change
            query_str = f"SELECT \"GSTIN\" FROM public.\"Comapny\" WHERE username = '{comapny_username}';"
            cur.execute(query_str)
            GSTIN = cur.fetchone()
            print(GSTIN)

            query_str = f"INSERT INTO public.\"Jobs\"( description, \"package\", num_of_openings, comapany_id, location,  name) VALUES ('{form.descrip.data}',{form.package.data}, {form.num_of_openings.data}, '{GSTIN[0]}', '{form.address.data}','{form.name.data}');"
            try:
                cur.execute(query_str)
                conn.commit()
                print("exectuted!")
                # print(session['username'])
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
            # print(session['username'])
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        redirect(url_for('home'))#** redirect to company
    return render_template('AddJobs.html',form=form)


@app.route('/jobinfo/<int:job_id>')
def job_info(job_id):
    query_str = f"SELECT * FROM public.\"Jobs\" where \"Job_ID\"={job_id}"
    cur.execute(query_str)
    res = cur.fetchone()
    job=[]
    for t in res:
        job.append(t)
    print(job)
    q1 = f"SELECT \"Seeker_id\" from public.\"Job_Application\" where job_id={job_id}"
    cur.execute(q1)
    applies = cur.fetchall()
    applied = [item for t in applies for item in t]
    print(applied)
    q1 = f"SELECT aadhar_number from public.\"Job_Seekers\" where username='{getSession()}'"
    cur.execute(q1)   
    an = cur.fetchone()[0] 
    if an in applied:
        yes = 1
    else:
        yes = 0
    print(yes)
    return render_template('jobInfo.html',job=json.dumps(job),yes=yes) 

@app.route('/jobinfo/<int:job_id>/applied')
def apply(job_id):
    js_username = getSession()
    print("hi")
    print(js_username)
    q1 = f"SELECT aadhar_number from public.\"Job_Seekers\" where username='{js_username}'"
    cur.execute(q1)   
    an = cur.fetchone()
    q2 = f"INSERT INTO public.\"Job_Application\" VALUES({an[0]},{job_id})"
    cur.execute(q2)
    conn.commit()
    return redirect(url_for('job_info',job_id=job_id))

@app.route('/jobinfo/<int:job_id>/cancel')
def cancel(job_id):
    js_username = getSession()
    print("hi")
    print(js_username)
    q1 = f"SELECT aadhar_number from public.\"Job_Seekers\" where username='{js_username}'"
    cur.execute(q1)   
    an = cur.fetchone()
    q2 = f"DELETE FROM public.\"Job_Application\" where \"Seeker_id\"={an[0]}"
    cur.execute(q2)
    conn.commit()
    return redirect(url_for('job_info',job_id=job_id))


@app.route('/jobappninfo/<int:job_id>')
def job_application_info(job_id):
    q1 = f"SELECT \"Seeker_id\" from public.\"Job_Application\" where job_id={job_id}"
    cur.execute(q1)
    applies = cur.fetchall()
    applied = [item for t in applies for item in t]
    print(applied)
    seekers=[]
    allskills=[]
    for i in range(len(applied)):
        q1 = f"SELECT * from public.\"Job_Seekers\" where aadhar_number={applied[i]}"
        cur.execute(q1)   
        an = cur.fetchone() 
        # print(an)
        s=[]
        for j in an:
            if j is None:
                s.append('-')
            else:
                s.append(j)
        # print(s)
        seekers.append(s)
        q2 =f"SELECT skill_id FROM public.seeker_skills where seeker_id='{applied[i]}'"
        cur.execute(q2)
        ab = cur.fetchall()
        skill=[]
        for j in ab:
            for k in j:
                skill.append(k)
        print(skill)
        skills=[]
        for j in skill:
            q3 = f"SELECT name from public.skills where skill_id={j}"
            cur.execute(q3)
            a=cur.fetchone()
            if a is not None:
                skills.append(a[0])
        allskills.append(skills)
        
    print(allskills)
    print(seekers)


    return render_template('jobAppnInfo.html',seekers=json.dumps(seekers),allskills=json.dumps(allskills))