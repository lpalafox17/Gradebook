from flask import Flask
from flask import request
from flask import jsonify
from flask import abort, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from sqlalchemy import delete
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grades.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model): #-------------------------------------------------------------
    __tablename__ = 'user'

    u_userID = db.Column(db.Integer, primary_key = True)
    u_username = db.Column(db.String, unique = True, nullable = False)
    u_password = db.Column(db.String, unique = True, nullable = False)
    
    def __init__(self, u_userID, u_username, u_password):
        self.u_userID = u_userID
        self.u_username = u_username
        self.u_password = u_password

class Student(db.Model): #-------------------------------------------------------------
    __tablename__ = 'student'

    s_studentID = db.Column(db.Integer, primary_key = True)
    s_studentName = db.Column(db.String, unique = True, nullable = False)
    s_userID = db.Column(db.Integer, unique = True, nullable = False)
    
    def __init__(self, s_studentID, s_studentName, s_userID):
        self.s_studentID = s_studentID
        self.s_studentName = s_studentName
        self.s_userID = s_userID

class Teacher(db.Model): #-------------------------------------------------------------
    __tablename__ = 'teacher'

    t_teacherID = db.Column(db.Integer, primary_key = True)
    t_teacherName = db.Column(db.String, unique = True, nullable = False)
    t_userID = db.Column(db.Integer, unique = True, nullable = False)

    def __init__ (self, t_teacherID, t_teacherName, t_userID):
        self.t_teacherID = t_teacherID
        self.t_teacherName = t_teacherName
        self.t_userID = t_userID

class Classes(db.Model): #-------------------------------------------------------------
    __tablename__ = 'classes'

    c_classID = db.Column(db.Integer, primary_key = True)
    c_courseName = db.Column(db.String, unique = True, nullable = False)
    c_teacherID = db.Column(db.Integer, unique = True, nullable = False)
    c_enrollNum = db.Column(db.Integer, unique = True, nullable = False)
    c_capacity = db.Column(db.Integer, unique = True, nullable = False)
    c_time = db.Column(db.String, unique = False, nullable = False)
    
    def __init__(self, c_classID, c_courseName, c_teacherID, c_enrollNum, c_capacity, c_time):
        self.c_classID = c_classID
        self.c_courseName = c_courseName
        self.c_teacherID = c_teacherID
        self.c_enrollNum = c_enrollNum
        self.c_capacity = c_capacity
        self.c_time = c_time

class Enrollment(db.Model): #-------------------------------------------------------------
    __tablename__ = 'enrollment'

    e_enrollID = db.Column(db.Integer, primary_key = True)
    e_classID = db.Column(db.String, unique = True, nullable = False)
    e_studentID = db.Column(db.Integer, unique = True, nullable = False)
    e_grade = db.Column(db.Float, unique = False, nullable = False)

    def __init__(self, e_enrollID, e_classID, e_studentID, e_grade):
        self.e_enrollID = e_enrollID
        self.e_classID = e_classID
        self.e_studentID = e_studentID
        self.e_grade = e_grade





@app.route('/')
def index():
    # return "Hello, This is the main page <h1>HELLO</h1>"
    return render_template('login.html')






if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    app.run(debug = True)