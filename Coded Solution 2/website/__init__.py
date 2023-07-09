from flask import Flask, url_for

def create_app():
    app = Flask(__name__) 
    app.config['SECRET_KEY'] = 'cookies'

    from .auth import auth
    from .views import views

    #Add the routes/paths to the application
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    return app