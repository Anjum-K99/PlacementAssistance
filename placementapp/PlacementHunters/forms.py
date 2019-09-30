from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, RadioField, DateField, IntegerField, DecimalField, SelectField, SelectMultipleField
from wtforms import FileField
from wtforms.validators import DataRequired,Length,Email,NumberRange, ValidationError, regexp
from flask_wtf.file import FileRequired
from PlacementHunters.model import Job_Seekers

class User_Registration(FlaskForm):
    aadhar_number = IntegerField('Aadhar Number',validators=[DataRequired(),NumberRange(min=000000000,max=999999999,message="Aadhar number must be 9 digits")])
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    firstname = StringField('First Name',validators=[DataRequired(),Length(min=2,max=20)])
    middlename = StringField('Middle Name',validators=[DataRequired(),Length(min=2,max=20)])
    lastname = StringField('Last Name',validators=[DataRequired(),Length(min=2,max=20)])
    address = TextAreaField('Address', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('M','Male'),('F','Female'),('O','Other')],validators=[DataRequired()])
    dob = DateField('Date Of Birth',validators=[DataRequired(),])
    mobile = IntegerField('Mobile Number',validators=[DataRequired(),NumberRange(min=7000000000,max=9999999999,message="Enter valid mobile number")])
    emailid = StringField('Email ID',validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_aadhar_number(self,aadhar_number):#name of function is important
        print("aadhar validation")
        number = Job_Seekers.query.filter_by(aadhar_no=aadhar_number.data).first()#none if there arent any
        if number:
            raise ValidationError('That aadhar number is taken. chose another. ')
    
    def validate_username(self,username):
        username = Job_Seekers.query.filter_by(username=username.data).first()#none if there arent any
        if username:
            raise ValidationError('That username is taken. chose another. ')

    

    def validate_emailid(self,emailid):
        email = Job_Seekers.query.filter_by(email=emailid.data).first()#none if there arent any
        if email:
            raise ValidationError('That email is taken. chose another. ')

# class academic_degree():
#     college_name = StringField('College/University Name',validators=[DataRequired(),Length(min=2,max=50)])
#     cgpa = DecimalField('CGPA',validators=[DataRequired(message="Enter valid percentage"),NumberRange(min=0,max=100,message="Enter valid perecentage")])
#     course_name = StringField('Course Name',validators=[DataRequired(),Length(min=2,max=50)])
#     year_of_passing = StringField('Year Of Passing',validators=[DataRequired(),Length(min=4,max=4)])



class User_Information(FlaskForm):
    school_name = StringField('School Name',validators=[DataRequired(),Length(min=2,max=50)])
    tenth_percent = DecimalField('10th Percentage',validators=[DataRequired(message="Enter valid percentage"),NumberRange(min=0,max=100,message="Enter valid perecentage")])
    junior_college_name = StringField('Junior College Name',validators=[DataRequired(),Length(min=2,max=50)])
    twelfth_percent = DecimalField('12th Percentage',validators=[DataRequired(message="Enter valid percentage"),NumberRange(min=0,max=100,message="Enter valid perecentage")])
    #graduation_info = academic_degree()
    graduation_college_name = StringField('College/University Name',validators=[DataRequired(),Length(min=2,max=50)])
    graduation_cgpa = DecimalField('CGPA',validators=[DataRequired(message="Enter valid percentage"),NumberRange(min=0,max=100,message="Enter valid perecentage")])
    graduation_course_name = StringField('Course Name',validators=[DataRequired(),Length(min=2,max=50)])
    graduation_year_of_passing = StringField('Year Of Passing',validators=[DataRequired()])
    #graduation_marksheet = FileField('Marksheet')

    post_graduation_yes_no =  RadioField('Add Post Graduation?', choices=[('Y','Yes'),('N','No')],validators=[DataRequired()])
    post_graduation_college_name = StringField('College/University Name')
    post_graduation_cgpa = DecimalField('CGPA')
    post_graduation_course_name = StringField('Course Name')
    post_graduation_year_of_passing = StringField('Year Of Passing')

    about_yourself = TextAreaField('About Yourself / Introduction', validators=[DataRequired()])
    hobbies = TextAreaField('Your hobbies', validators=[DataRequired()])
    skills = SelectMultipleField('Your Skills',choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class Home_form(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=50)])
    password = PasswordField('Password',validators=[DataRequired()])
    login = SubmitField('Login')
    register = SubmitField('Register')
    # Your form's submit button's data value will be True if it was pressed. See very simple example below of a form with two submit buttons and a single input field.



