#! /usr/bin/python3

from flask import Flask, abort, render_template, url_for, request, redirect, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import jsonify
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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
    id = db.Column(db.Integer, primary_key = True, unique = True)
    courseName = db.Column(db.String(100), unique = True, nullable = False)
    teacherID = db.Column('teacherID', db.ForeignKey(Teacher.id), nullable = False)
    enrollNum = db.Column(db.Integer, unique = True, nullable = False)
    capacity = db.Column(db.Integer, unique = True, nullable = False)
    time = db.Column(db.String(100), unique = False, nullable = False)
    teacher = db.relationship('Teacher', backref = ('Courses'))

class Enrollment(db.Model): #-------------------------------------------------------------
    ____tablename__ = 'Enrollment'
    id = db.Column(db.Integer, primary_key = True, unique = True)
    courseID = db.Column('courseID', db.ForeignKey(Courses.id))
    studentID = db.Column('studentID', db.ForeignKey(Student.id))
    grade = db.Column(db.Integer, unique = False)
    course = db.relationship('Courses', backref = ('Enrollment'))
    student = db.relationship('Student', backref = ('Enrollment'))



class RegistrationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=25)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=25)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists. Please choose a different one.")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=25)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=25)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


@app.route('/')
def index():
    # return "Hello, This is the main page <h1>HELLO</h1>"
    return render_template('home.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


    # return "Hello, This is the main page <h1>HELLO</h1>"
    # return render_template('login.html', form = form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



# register flask-admin with app
admin = Admin(app)

# create a view of flask-admin according to the database
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Teacher, db.session))
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Courses, db.session))
admin.add_view(ModelView(Enrollment, db.session))

if __name__ == "__main__":
   #db.drop_all()
  #  db.create_all()
    app.run(debug = True)
