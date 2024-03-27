from webapp import db,bcrypt

from datetime import *
from pytz import timezone
uae = timezone('Asia/Dubai')

from flask_login import UserMixin,current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import url_for,redirect

from flask_admin import BaseView, expose

from wtforms import TextAreaField
from wtforms.widgets import TextArea


from sqlalchemy import inspect
from sqlalchemy.orm import backref

from webapp.admin_views import *


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return self.username
    
    # You can create your own custom properties here
    # Can be used in place of Jinja Template Filters

    @property
    def password_check(self):
        return self.password_check
    
    @password_check.setter
    def password_check(self,text_password):
        self.password = bcrypt.generate_password_hash(text_password).decode('utf-8')

    def check_password(self,attempted_password):
        return bcrypt.check_password_hash(self.password,attempted_password)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentName = db.Column(db.String(100), unique=True)

    email = db.Column(db.String(100), unique=True)
    
    company = db.Column(db.String(100))
    profession = db.Column(db.String(100))

    created_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))

    def __repr__(self):
        return self.studentName

class Course(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    courseName = db.Column(db.String,nullable = True)
    courseDescription = db.Column(db.Text(),nullable = True)
    courseImage = db.Column(db.String,nullable = False)

    assignment = db.Column(db.Boolean)
    assignment_frequency = db.Column(db.Integer)

    created_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(uae))
    modified_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(uae))

    def __repr__(self):
        return self.courseName

class UserCourse(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.Integer,db.ForeignKey('user.id'))
    courseId = db.Column(db.Integer,db.ForeignKey('course.id'))

    course = db.relationship('Course', backref=db.backref('user', lazy='dynamic'))
    user = db.relationship('User', backref=db.backref('course', lazy='dynamic'))
    
    created_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))
    modified_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    courseId = db.Column(db.Integer,db.ForeignKey('course.id'))

    lessonName = db.Column(db.String,nullable = True)
    lessonDescription = db.Column(db.Text(),nullable = True)

    game = db.Column(db.String,nullable = True)

    sampleCode1 = db.Column(db.String,nullable = True)
    sampleCode2 = db.Column(db.String,nullable = True)
    sampleCode3 = db.Column(db.String,nullable = True)
    sampleCode4 = db.Column(db.String,nullable = True)
    resources = db.Column(db.String,nullable = True)

    lessonOrder = db.Column(db.Integer, nullable = False)

    course = db.relationship('Course', backref=db.backref('lesson', lazy='dynamic'))

    created_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(uae))
    modified_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(uae))

    def __repr__(self):
        return self.lessonName

class QuizMaster(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String,nullable = False)

    created_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(uae))
    modified_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(uae))

    def __repr__(self):
        return self.question
    
class SurveyMaster(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String,nullable = False)

    created_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(uae))
    modified_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(uae))

    def __repr__(self):
        return self.question

class QuizResults(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question_id = db.Column(db.Integer,db.ForeignKey('quiz_master.id'))

    student_id  = db.Column(db.Integer,db.ForeignKey('student.id'))
    course_id  = db.Column(db.Integer,db.ForeignKey('course.id'))
    
    response = db.Column(db.Integer,nullable = False)

    quizmaster = db.relationship('QuizMaster', backref=db.backref('quiz_results', lazy='dynamic'))
    student = db.relationship('Student', backref=db.backref('quiz_results', lazy='dynamic'))
    course = db.relationship('Course', backref=db.backref('quiz_results', lazy='dynamic'))

    created_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))
    modified_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))

class SurveyResults(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question_id = db.Column(db.Integer,db.ForeignKey('survey_master.id'))

    student_id  = db.Column(db.Integer,db.ForeignKey('student.id'))
    course_id  = db.Column(db.Integer,db.ForeignKey('course.id'))
    
    response = db.Column(db.String,nullable = False)

    surveymaster = db.relationship('SurveyMaster', backref=db.backref('survey_results', lazy='dynamic'))
    student = db.relationship('Student', backref=db.backref('survey_results', lazy='dynamic'))
    course = db.relationship('Course', backref=db.backref('survey_results', lazy='dynamic'))

    created_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))
    modified_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    activityName  = db.Column(db.String,nullable = False)
    activityImage = db.Column(db.String,nullable = False)
    activityURL = db.Column(db.String,nullable = False)

class FeedbackRating(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    objective = db.Column(db.Integer)
    comments = db.Column(db.String(500))

    created_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))
    modified_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))

class FeedbackFeature(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    feature = db.Column(db.String(100))

class FeedbackFeatureOutcome(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer)
    feature_id = db.Column(db.Integer)
    outcome = db.Column(db.Integer)

    created_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))
    modified_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    name  = db.Column(db.String,nullable = False)
    theme = db.Column(db.String,nullable = False)
    question = db.Column(db.String,nullable = False)
    response = db.Column(db.Integer,nullable = False)

    created_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))
    modified_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))
