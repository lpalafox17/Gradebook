from flask import Flask, abort, render_template, url_for, request, redirect, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import jsonify
# from flask_login import UserMixin

app = Flask(__name__)

# with app.app_context():
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(db.Model): #-------------------------------------------------------------
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(100), unique = True, nullable = False)


class Student(db.Model): #-------------------------------------------------------------
    __tablename__ = 'Student'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    userID = db.Column('userID', db.ForeignKey(User.id), nullable = False)
    user = db.relationship('User', backref=db.backref('Student', uselist=False))


class Teacher(db.Model): #-------------------------------------------------------------
    __tablename__ = 'Teacher'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    userID = db.Column('userID', db.ForeignKey(User.id), nullable = False)
    user = db.relationship('User', backref=db.backref('Teacher', uselist=False))


class Courses(db.Model): #-------------------------------------------------------------
    __tablename__ = 'Courses'
    id = db.Column(db.Integer, primary_key = True)
    courseName = db.Column(db.String(100), unique = True, nullable = False)
    teacherID = db.Column('teacherID', db.ForeignKey(Teacher.id), nullable = False)
    enrollNum = db.Column(db.Integer, unique = True, nullable = False)
    capacity = db.Column(db.Integer, unique = True, nullable = False)
    time = db.Column(db.String(100), unique = False, nullable = False)
    teacher = db.relationship('Teacher', backref = ('Courses'))


class Enrollment(db.Model): #-------------------------------------------------------------
    ____tablename__ = 'Enrollment'
    id = db.Column(db.Integer, primary_key = True)
    courseID = db.Column('courseID', db.ForeignKey(Courses.id))
    studentID = db.Column('studentID', db.ForeignKey(Student.id))
    grade = db.Column(db.Integer, unique = False)
    course = db.relationship('Courses', backref = ('Enrollment'))
    student = db.relationship('Student', backref = ('Enrollment'))


@app.route('/')
def index():
    # return "Hello, This is the main page <h1>HELLO</h1>"
    return render_template('home.html')


@app.route('/login')
def login():
    # return "Hello, This is the main page <h1>HELLO</h1>"
    return render_template('login.html')


# register flask-admin with app
admin = Admin(app)
# create a view of flask-admin according to the database
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Teacher, db.session))
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Courses, db.session))
admin.add_view(ModelView(Enrollment, db.session))

if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    app.run(debug = True)
