from flask import Blueprint, render_template, request, flash, jsonify, abort, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
# from flask_cors import CORS
from .models import Teachers, Classes, Students, Enrollment
from more_itertools import flatten
from sqlalchemy import desc
from .__init__ import needAPP
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint('views', __name__)



@views.route('/login', methods=['GET', 'POST'])
@login_required
def home():

    teacherID = list(flatten(Teachers.query.with_entities(Teachers.User_id).order_by(desc(Teachers.id)).all()))
    studentID = list(flatten(Students.query.with_entities(Students.User_id).order_by(desc(Students.id)).all()))

    if(current_user.id in teacherID):
        return redirect(url_for('views.instructor', name = current_user.username))
    elif(current_user.id in studentID):
        return redirect(url_for('views.student', name = current_user.username))
    elif (current_user.id == 1):
        return redirect(url_for('admin.index'))

    return render_template("base.html", current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('home/instructor/<name>')
@login_required
def instructor(name):
        
    tea_data = []
    teaQ = Teachers.query.filter_by(Name=name).first()
    print(current_user.id)
    print(teaQ.User_id)
    if current_user.id != teaQ.User_id:
        abort(403)
    
    teaQC = Classes.query.filter_by(teacher_id = teaQ.id).all()
    for i in range(len(teaQC)):
        temp = {
            'CourseName':teaQC[i].course_name,
            'Teacher':name,
            'Time':teaQC[i].time,
            'StudentsEnrolled':(str(teaQC[i].numberEnrolled) + "/" + str(teaQC[i].capacity))
        }
        tea_data.append(temp)
    
    return render_template("instructor.html", instructor_name = name, data = tea_data)


@views.route("home/instructor/<name>/<course>", methods = ['GET', 'POST'])
@login_required
def specific_course(name, course, student = None):
    instructor_name = name
    instructor_course = course

    tea_course_data = []
    teaQ = Teachers.query.filter_by(Name=instructor_name).first()
    teaQC = Classes.query.filter_by(teacher_id = teaQ.id, course_name = instructor_course).first()

    teaQD = Enrollment.query.filter_by(class_id = teaQC.id).all()
    print(teaQC)
    print(teaQD)

    if request.method == 'GET':
        # Displays grades for a specific course
        
        for j in range(teaQC.numberEnrolled):
            studentSpecClass = Students.query.filter_by(id = teaQD[j].student_id).first()
            print(studentSpecClass)
            temp1 = {
                'name':studentSpecClass.Name,
                'grade':teaQD[j].grade
            }
            tea_course_data.append(temp1)

    if request.method == 'POST':
        student_id = Students.query.filter_by(Name = request.args.get('student')).first().id
        course_id = Classes.query.filter_by(course_name = instructor_course).first().id

        Enrollment.query.filter_by(student_id = student_id, class_id = course_id).update({'grade': (request.form.get('new_grade'))})
        db.session.commit()

        for j in range(teaQC.numberEnrolled):
            studentSpecClass = Students.query.filter_by(id = teaQD[j].student_id).first()
            temp1 = {
                'name':studentSpecClass.Name,
                'grade':teaQD[j].grade
            }
            tea_course_data.append(temp1)
    

    return render_template("specificCourse.html", instructor_name = instructor_name, instructor_course = instructor_course, data = tea_course_data)


@views.route("home/student/<name>", methods = ['POST', 'GET'])
#@login_required
def student(name):
    student_name = name

    try_data = []
        
    # get all courses the student is enrolled in
    if request.method == 'GET':
        stuQ = Students.query.filter_by(Name=student_name).first()
        
        if not stuQ:
            abort(404)
        elif(current_user.id != stuQ.User_id):
            abort(403)

        stuQC = Enrollment.query.filter_by(student_id = stuQ.id).all()

        for i in range(len(stuQC)):
            stuClass = Classes.query.filter_by(id = stuQC[i].class_id).all()
   
            teachName = Teachers.query.filter_by(id = stuClass[0].teacher_id).all()
            print(teachName)

            temp = {
                'CourseName':stuClass[0].course_name,
                'Teacher':teachName[0].Name,
                'Time':stuClass[0].time,
                'StudentsEnrolled':(str(stuClass[0].numberEnrolled) + "/" + str(stuClass[0].capacity))
            }
            try_data.append(temp)
        
    # add or remove a course
    elif request.method == 'POST': 
        course_name = request.form.get('course_name')
        enroll_option = request.form.get('enroll_option')

        stuQ = Students.query.filter_by(Name=student_name).first()
        courseReqNm = course_name
        courseReq = Classes.query.filter_by(course_name = courseReqNm).first()

        if enroll_option == 'add':
            # update the enrollment count
            Classes.query.filter_by(course_name = courseReqNm).update({'numberEnrolled': (Classes.numberEnrolled + 1)})
            newCourseStu = Enrollment(student_id = stuQ.id, class_id = courseReq.id, grade = "")
            db.session.add(newCourseStu)

        elif enroll_option == 'remove':
            Classes.query.filter_by(course_name = courseReqNm).update({'numberEnrolled': (Classes.numberEnrolled - 1)})
            enrollmentReq = Enrollment.query.filter_by(student_id = stuQ.id, class_id = courseReq.id).first()
            
            db.session.delete(enrollmentReq)


        db.session.commit()
    
    return render_template("student.html", student_name = student_name, data = try_data)


@views.route("/enrolled/<name>")
def enrolled(name, methods = ['POST', 'GET']):
    try_data = []
    if request.method == 'GET':
        stuQ = Students.query.filter_by(Name=name).first()

        stuQC = Enrollment.query.filter_by(student_id = stuQ.id).all()

        for i in range(len(stuQC)):
            stuClass = Classes.query.filter_by(id = stuQC[i].class_id).all()
    
            teachName = Teachers.query.filter_by(id = stuClass[0].teacher_id).all()
            temp = {
                'name':stuClass[0].course_name,
                'instructor':teachName[0].Name,
                'time':stuClass[0].time,
                'enrollment':(str(stuClass[0].numberEnrolled) + "/" + str(stuClass[0].capacity)),
            }
            try_data.append(temp)
    
    return jsonify(try_data)


@views.route("/courses")
def courses():
    try_data = []
    courseQ = Classes.query.all()

    for i in range(len(courseQ)):
        teachName = Teachers.query.filter_by(id = courseQ[i].teacher_id).all()

        temp = {
            'name':courseQ[i].course_name,
            'instructor':teachName[0].Name,
            'time':courseQ[i].time,
            'enrollment':(str(courseQ[i].numberEnrolled) + "/" + str(courseQ[i].capacity))
        }
        try_data.append(temp)
    return jsonify(try_data)


