from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1998@localhost/ruv'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://exjnqvukactnfg:3b8f883ff3c761a6c55cf99889e502a6a77fb7a03141eea3601ee23f92f36634@ec2-34-200-94-86.compute-1.amazonaws.com:5432/db6ul13r76r128'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    EmailID= db.Column(db.String(200),unique=True)
    Employee = db.Column(db.String(200),primary_key=True )
    Location = db.Column(db.String(200))
    EmployeeID = db.Column(db.String(200), unique=True)
    Designation = db.Column(db.String(200))
    Department = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self,EmailID,Employee,Location,EmployeeID,Designation, Department, rating, comments):
        self.EmailID = EmailID
        self.Employee = Employee
        self.Location = Location
        self.EmployeeID = EmployeeID
        self.Designation = Designation
        self.Department = Department
        self.rating = rating
        self.comments = comments 

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
         EmailID = request.form['EmailID']
         Employee = request.form['Employee']
         Location = request.form['Location']
         EmployeeID = request.form['EmployeeID']
         Designation = request.form['Designation']
         Department = request.form['Department']
         rating = request.form['rating']
         comments = request.form['comments']
        # print(employee, department, rating, comments)
         if Employee == '' or Department == '':   
            return render_template('index.html', message='Please enter required fields')
         if db.session.query(Feedback).filter(Feedback.Employee == Employee).count() == 0:
            data = Feedback(EmailID,Employee,Location,EmployeeID,Designation, Department, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(EmailID,Employee,Location,EmployeeID,Designation, Department, rating, comments)
            return render_template('success.html')
        
         return render_template('index.html', message='You have already submitted feedback')


if __name__ == '__main__':
    app.run()
    
    
    
    
    

