#! /usr/bin/python3

from flask import Flask, abort, render_template, url_for, request, redirect, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
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
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# admin = Admin(app, index_view=MyAdminModelView)
admin = Admin(app)



class User(db.Model, UserMixin): #-------------------------------------------------------------
    id = db.Column('id', db.Integer, primary_key = True)
    username = db.Column('username', db.String(100))
    password = db.Column('password', db.String(100))
    def __repr__(self):
        return '<User %r>' % (self.username)

class Student(db.Model): #-------------------------------------------------------------
    __tablename__ = 'Student'
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(100))
    user_id = db.Column('user_id', db.ForeignKey('user.id'), nullable = False)
    user = db.relationship('User', backref=db.backref('Student', uselist=False))
    def __repr__(self):
        return '<Student %r>' % (self.user_id)

class StudentView(ModelView):
    column_list = ['user.username', 'name']

class Teacher(db.Model): #-------------------------------------------------------------
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(100), unique = True)
    user_id = db.Column('user_id', db.ForeignKey('user.id'), nullable = False)
    user = db.relationship('User', backref=db.backref('Teacher', uselist=False))
    def __repr__(self):
        return '<Teacher %r>' % (self.user_id)

class TeacherView(ModelView):
    column_list = ['user.username', 'name']

class Courses(db.Model): #-------------------------------------------------------------
    __tablename__ = 'Courses'
    id = db.Column('id', db.Integer, primary_key = True)
    courseName = db.Column('courseName', db.String(100))
    teacher_id = db.Column('teacher_id', db.ForeignKey('teacher.id'), nullable = False)
    enrollNum = db.Column('enrollNum', db.Integer)
    capacity = db.Column('capacity', db.Integer)
    time = db.Column('time', db.String(100))
    teacher = db.relationship('Teacher', backref=db.backref('Courses'))
    def __repr__(self):
        return '<Courses %r>' % (self.id)

class CoursesView(ModelView):
    column_list = ['courseName', 'teacher.name', 'enrollNum', 'capacity', 'time']

class Enrollment(db.Model): #-------------------------------------------------------------
    ____tablename__ = 'Enrollment'
    id = db.Column('id', db.Integer)
    course_id = db.Column('course_id', db.ForeignKey('Courses.id'), primary_key = True)
    student_id = db.Column('student_id', db.ForeignKey('Student.id'), primary_key = True)
    grade = db.Column('grade', db.Integer)
    courses = db.relationship('Courses', backref=db.backref('Enrollment'))
    student = db.relationship('Student', backref=db.backref('Enrollment'))
    def __repr__(self):
        return '<Enrollment %r>' % (self.student_id)

class EnrollmentView(ModelView):
    column_labels = {'student.name': 'Student'}
    column_list = ['student.name', 'course.courseName', 'grade']



#-- Admin Model View for Tables ----------------------------------------------
admin.add_view(ModelView(User, db.session))
admin.add_view(StudentView(Student, db.session))
admin.add_view(TeacherView(Teacher, db.session))
admin.add_view(CoursesView(Courses, db.session))
admin.add_view(EnrollmentView(Enrollment, db.session))


#--Flask Login-in Form-------------------------------------------------------
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')



@app.route('/') #--------------------------------------------- HOME ROUTE --
def home():
    # return "Hello, This is the main page <h1>HELLO</h1>"
    return render_template('home.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # if bcrypt.check_password_hash(user.password, form.password.data):
            if user.password == form.password.data:
                student = db.session.query(User).join(Student).filter(User.id == user.id).all()
                teacher = db.session.query(User).join(Teacher).filter(User.id == user.id).all()
                if student:
                    login_user(user)
                    # return redirect(url_for('dashboard'))
                    return redirect('/student')
                elif teacher:
                    login_user(user)
                    return redirect('/teacher')
                else:
                    login_user(user)
                    return redirect(url_for('admin.index'))
    return render_template('login.html', form=form)

@app.route('/getstudentcourses', methods=['GET'])
def getStudentCourses():
    student = Student.query.filter_by(user_id = current_user.id).first()
    output = db.session.query(Student, Courses, Enrollment)\
        .filter(Student.id == Enrollment.student_id)\
        .filter(Courses.id == Enrollment.course_id)\
        .filter(Student.id == student.id).all()
    specificStudentCourses = {}
    for course in output:
        specificStudentCourses.update({course.Enrollment.id : \
            (course.Courses.courseName,
            course.Courses.teacher.name,
            course.Courses.time,
            str(course.Courses.enrollNum) + '/' + str(course.Courses.capacity))})
        return specificStudentCourses


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/student', methods=['GET', 'POST'])
def student():
    user = current_user.id
    studentLogged = Student.query.filter_by(user_id=user).first()
    s = studentLogged.id
    return render_template('student.html')


@app.route('/teacher', methods=['GET', 'POST'])
def teacher():
    #user = current_user.id
    #studentLogged = Student.query.filter_by(user_id=user).first()
    #s = studentLogged.id
    return render_template('teacher.html')


if __name__ == "__main__":
    # db.drop_all()
    # db.create_all()
    app.run(debug = True)
