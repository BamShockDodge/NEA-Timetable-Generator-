#Contains normal Routes
from flask import Blueprint, render_template
from flask_login import login_required, current_user


views = Blueprint('views', __name__) 
@views.route('/')
def main():
    return render_template("main.html")

@views.route('/home')
@login_required
def home():
    return render_template("home.html")
