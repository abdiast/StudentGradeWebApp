from flask import Flask 
from flask_admin import Admin, AdminIndexView, expose
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user, UserMixin
from flask_security import Security, SQLAlchemyUserDatastore, \
	RoleMixin, login_required, current_user
from . import db
import json
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import BaseModelView
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
from sqlalchemy import inspect

from .models import *

class Administrator(ModelView):
	@login_required
	def is_accessible(self):
		return super().is_accessible()

	column_display_pk = True
	column_hide_backrefs = False
	column_list = []


listOfModels = [Role, Users, Students, Teachers,Classes, Enrollment]

AllColList = []
for i in range(len(listOfModels)):
	AllColList.append([c_attr.key for c_attr in inspect(listOfModels[i]).mapper.column_attrs])


# print(AllColList)
# class AView(ModelView):
# 	column_display_pk = True 
# 	column_hide_backrefs = False
# 	#property, all columns except primary key will be shown
# 	column_list = [c_attr.key for c_attr in inspect(Students).mapper.column_attrs]
# 	print(column_list)


# class BView(ModelView):
#     column_list('b1','b2')

    




class MyAdminView(AdminIndexView):
	def is_accessible(self):
		print(current_user)
		return (current_user.is_active and
				current_user.is_authenticated and
				current_user.has_roles('superuser')
		)
	@expose('/')
	def index(self):
		arg1 = 'Hello'
		return self.render('adminhome.html', arg1=arg1)
	# def inaccessible_callback(self, name, **kwargs):
	#     return redirect(url_for('auth.login'))


user_datastore = SQLAlchemyUserDatastore(db, Users, Role)

def appnamey(Daname):
	admin = Admin(Daname, name='Admin', template_mode='bootstrap3', index_view=MyAdminView()) 
	for j in range(len(AllColList)):
		daSesh = db.session
		tempAdmin = Administrator(listOfModels[j], daSesh)

		tempAdmin.column_list = AllColList[j]

		admin.add_view(tempAdmin)


	# admin.add_view(Administrator(Users, db.session)) 
	# admin.add_view(Administrator(Teachers, db.session)) 
	# admin.add_view(Administrator(Students, db.session)) 
	# admin.add_view(Administrator(Classes, db.session)) 
	# admin.add_view(AView(Students, db.session))


def superuserNewDB(Daname):
	with Daname.app_context():
		user_role = Role(name='user')
		super_user_role = Role(name='superuser')
		db.session.add(user_role)
		db.session.add(super_user_role)
		db.session.commit()

	
		test_user = user_datastore.create_user(
			username='Admin',
			email='admin@admin.com',
			password = generate_password_hash('admin', method='sha256'),
			roles=[user_role, super_user_role]
			)
		db.session.commit()