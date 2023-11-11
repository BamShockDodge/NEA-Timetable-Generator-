#Contains normal Routes
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from website import CSPSolver

#Creates routes for website
views = Blueprint('views', __name__) 
#Decorator for main function
@views.route('/')
def main():
    return render_template("main.html")

#Decorate for home function
@views.route('/home')
#Decorator that states that login is required
@login_required
#Function loads home.html webpage when called
def home():
    return render_template("home.html")

@views.route("/selection")
@login_required
def selection():
    return render_template("selection.html", timetable1 = CSPSolver.timetable1, timetable2 = CSPSolver.timetable2, timetable3 = CSPSolver.timetable3)
    