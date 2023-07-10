#Authentication routes
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
#Imports encrpytion algorithm and hashing
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__) 

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password1 = request.form.get("password1")
        #Queries the database for username and return first result
        user = User.query.filter_by(username=username).first()
        if user:
            #If user password in database matches password1 entered grant access
            if check_password_hash(user.password, password1):
                flash('Login Successful', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Username does not exist', category='error')

    return render_template("login.html")

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        #Basic validation implement proper functions later
        user_email = User.query.filter_by(email=email).first()
        user_username = User.query.filter_by(username=username).first()
        if user_email:
            flash('Email already registered', category='error')
        elif user_username:
            flash('Username is taken choose another one', category='error')
        elif len(email) <= 4:
            flash('Email must be more than 4 characters', category="error")
        elif len(firstname) <= 2:
            flash('First Name must be more than 2 characters', category="error")
        elif len(lastname) <= 2:
            flash('Last Name must be more than 2 characters', category="error")
        elif len(username) <= 7:
            flash('Username must be more than 7 characters', category="error")
        elif password1 !=  password2:
            flash('Passwords must match', category="error")
        elif len(password1) <= 7:
            flash('Password must be more than 7 characters', category="error")
        else:
            new_user = User(email=email, firstname=firstname, lastname=lastname, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
            

    return render_template("register.html")

@auth.route('logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))