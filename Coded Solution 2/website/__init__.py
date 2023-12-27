#import flask module
from flask import Flask, url_for
#imports database module
from flask_sqlalchemy import SQLAlchemy
#imports the flask login module
from flask_login import LoginManager

#database is defined and given a name
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    #Flask app is defined
    app = Flask(__name__) 
    app.config['SECRET_KEY'] = 'cookies'

    #Database stored here
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #Database is intialised
    db.init_app(app)

    #Imports all the website routes from other python files
    from .auth import auth
    from .views import views

    #Add the routes/paths to the application
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #Import database and tables
    from .models import User, Timetable

    #Creates the database
    with app.app_context():
        db.create_all()

    #Initalises login_manager
    login_manager = LoginManager()
    #If login required redirect to auth.login
    login_manager.login_view = 'auth.login '
    login_manager.init_app(app)

    #Loads specific user by getting primary key
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    #Flask application is returned
    return app