from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(150), unique=True)
#     password = db.Column(db.String(150))
#     first_name = db.Column(db.String(150))
#     #notes = db.relationship('Note')

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(150))
    notes = db.relationship('Note')
    def __repr__(self):
            return '<User %r>' % self.username

class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(150))
    User_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(150))
    User_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(150), unique=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    numberEnrolled = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    time = db.Column(db.String(50))

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    grade = db.Column(db.String(50))