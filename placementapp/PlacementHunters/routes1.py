from PlacementHunters import app
from flask import Flask, render_template, redirect, url_for
import json
from PlacementHunters.forms import Home_form,Company_reg
# from PlacementHunters.forms import Job_Seeker, User_Information, Home_form

#for psycopg:
import psycopg2
conn = psycopg2.connect("dbname=JobHunters user=postgres password=kjsce")
cur = conn.cursor()
print("connection successful",conn)

@app.route('/')
@app.route('/home')
def home():
    form = Home_form() #insatnce of form
    print("main route")
    return render_template("landingPage.html", title="Home",form=form)



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

@app.route('/CompanyReg',methods=['GET','POST'])
def Company_registration():
    form = Company_reg()
    if form.validate_on_submit():
        print("company form valid")
        try:
            query_str = f"INSERT INTO public.\"Comapny\"(\"GSTIN\",name, username, mobile, location, password, website) VALUES ({int(form.GSTIN.data)}, '{form.name.data}', '{form.username.data}', '{form.mobile.data}', '{form.address.data}',' {form.password.data}', '{form.website.data}')"
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