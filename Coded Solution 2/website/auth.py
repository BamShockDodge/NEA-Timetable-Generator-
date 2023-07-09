#Authentication routes
from flask import Blueprint, render_template, request, flash, redirect
auth = Blueprint('auth', __name__) 

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password1 = request.form.get("password1")
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
        
        if len(email) <= 4:
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
            flash('Account created!', category='success')
            return redirect('home')
            

    return render_template("register.html")