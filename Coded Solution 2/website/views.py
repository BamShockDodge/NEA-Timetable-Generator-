#Contains normal Routes
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from website import auth

#Creates routes for website
views = Blueprint('views', __name__) 
#Decorator for main function
@views.route('/')
def main():
    return render_template("main.html")

#Decorate for start function
@views.route('/start')
#Decorator that states that login is required
@login_required
#Function loads start.html webpage when called
def start():
    return render_template("start.html")

#Decorate for home function
@views.route('/home')
#Decorator that states that login is required
@login_required
#Function loads start.html webpage when called
def home():
    return render_template("home.html", current_timetable = auth.current_timetable)


    