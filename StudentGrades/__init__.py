from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_cors import CORS

db = SQLAlchemy()
DB_NAME = "StudentEnrollment.sqlite"

app = Flask(__name__)

def create_app():
    #app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['FLASK_ADMIN_SWATCH'] = 'United'

    db.init_app(app)

    from .views import views
    from .auth import auth
    from .admin import appnamey

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Note, Teachers, Students, Classes, Enrollment, Users
    appnamey(app)
    
    create_database(app)

    # from .newCourseReceiver import pytojs
    # pytojs(app)
    CORS(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
            from .admin import superuserNewDB
            superuserNewDB(app)
    
        print('Created Database!')

def needAPP():
    return app
