from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemyUserDatastore, \
    RoleMixin, login_required, current_user
from sqlalchemy import UniqueConstraint

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


roles_users = db.Table(
    'roles_users',
    db.Column('users_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(150))
    active = db.Column(db.Boolean())
    notes = db.relationship('Note')
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
        
    def has_roles(self, *args):
        return set(args).issubset({role.name for role in self.roles})
                            
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
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), unique=True)
    grade = db.Column(db.String(50))
    #UniqueConstraint(class_id, student_id)

