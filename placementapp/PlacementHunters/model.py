from PlacementHunters import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader#so the extension knows that this is the function to get a user by their id. 
def load_seeker(aadhar_no):#for reloading the user stored in the user_id in the session 
    #bc the extension needs to know how to find the user by the id.
    return Job_Seekers.query.get(int(aadhar_no))


class Job_Seekers(db.Model,UserMixin):
    aadhar_no = db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True, nullable=False)
    password = db.Column(db.String(30),unique=True, nullable=False)

    #details:
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    email = db.Column(db.String(120), unique=True, nullable=False)

    ##
    def __repr__(self):
        return f"Job_seeker('{self.username}', '{self.email}', '{self.image_file}')"
    
    def get_id(self):
           return (self.aadhar_no)

class Companies(db.Model,UserMixin):
    gstin_no = db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True, nullable=False)
    password = db.Column(db.String(30),unique=True, nullable=False)

    #details:
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    email = db.Column(db.String(120), unique=True, nullable=False)

    ##
    def __repr__(self):
        return f"Comapny('{self.username}', '{self.email}', '{self.image_file}')"
