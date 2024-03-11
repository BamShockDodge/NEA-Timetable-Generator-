#Authentication routes
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Timetable
#Imports encrpytion algorithm and hashing
from werkzeug.security import generate_password_hash, check_password_hash
#Imports the database
from . import db
#Imports the flask login module
from flask_login import login_user, login_required, logout_user, current_user
from website import generator_values
from website import generator

#Creates the routes for the website 
auth = Blueprint('auth', __name__) 

#Decorator for login function which is path on the website
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    #Html file uses POST request so any information used in html file can be accessed here
    if request.method == "POST":
        #Username and password entered is collected from request form of html file
        username = request.form.get("username")
        password1 = request.form.get("password1")
        #Queries the database for username and return first result
        user = User.query.filter_by(username=username).first()
        if user:
            #If user password in database matches password1 entered grant access
            if check_password_hash(user.password, password1):
                flash('Login Successful', category='success')
                login_user(user, remember=True)
                
                #Gets Row from dicionary table using the user_id as a foreign key
                timetable = Timetable.query.filter_by(user_id=user.id).first()

                #if there is no timetable connected to user id redirect to start page
                if timetable == None:
                    return redirect(url_for('views.start'))
                #if there is a timetable connected to user id redirect to home page
                else:
                    return redirect(url_for('views.home', timetable=timetable.data))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Username does not exist', category='error')
    #If user does not enter correct information they are sent back to login page
    return render_template("login.html", user=current_user)

#Decorator for register function which is path on the website
@auth.route('/register', methods = ['GET', 'POST'])
def register():
    #Html file uses POST request so any information entered in html file can be accessed here
    if request.method == "POST":
        #Create variables using data from html files as the values
        email = request.form.get("email")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        #Checks that all user entered data is valid and follows all rules
        email_valid = ValidateEmail(email)
        username_valid = ValidateUsername(username)
        password_valid = ValidatePassword(password1, password2)
        if (email_valid == True and username_valid == True and password_valid == True):
            #Creates a new user in database using data and encrypts password using hashing function
            new_user = User(email=email, 
            firstname=firstname, 
            lastname=lastname, 
            username=username, 
            password=generate_password_hash(password1, method='sha256'))
            #Adds the new_user to the database
            db.session.add(new_user)
            #This change is saved
            db.session.commit()
            #The user is then logged in
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            #User redirected to start page after registering
            return redirect(url_for('views.start'))
            
    #Reloads the registering page
    return render_template("register.html", user=current_user)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


#Assigns entered web data into arrays
@auth.route('/input', methods = ['GET', 'POST'])
@login_required
def input():
    if request.method == "POST":
        #All Names and confidences are used as attributes to create subject objects
        generator_values.subjects.append(generator_values.Subject(request.form.get("subject1"), request.form.get("confidence1")))
        generator_values.subjects.append(generator_values.Subject(request.form.get("subject2"), request.form.get("confidence2")))
        generator_values.subjects.append(generator_values.Subject(request.form.get("subject3"), request.form.get("confidence3")))
        if (request.form.get("subject4") != ''):
            generator_values.subjects.append(generator_values.Subject(request.form.get("subject4"), request.form.get("confidence4")))

        #The day IDs correspond to the time available each day IDs
        hours_available = {
        'monday': 'time1',
        'tuesday': 'time2',
        'wednesday': 'time3',
        'thursday': 'time4',
        'friday': 'time5',
        'saturday': 'time6',
        'sunday': 'time7'
        }
        #The days the student is available is stored in a dictionary
        for key in generator_values.days_available.keys():
            #If the box is checked the student is available on that day
            if request.form.get(key) == 'on':
                generator_values.days_available[key][0] = True
                #Gets the time available to revise on that day and adds to the dictionary
                generator_values.days_available[key][1] = request.form.get(hours_available[key])
            else:
                generator_values.days_available[key][0] = False

        #Calls the generator_values function clean data
        generator_values.clean_data()
        
        return redirect(url_for('auth.selection'))


    return render_template("timetableinputs.html")


@auth.route("/selection",  methods = ['GET', 'POST'])
@login_required
def selection():
    if request.method == "POST":
        checkboxes = []
        checkboxes.append(request.form.get("timetable1"))
        checkboxes.append(request.form.get("timetable2"))
        checkboxes.append(request.form.get("timetable3"))
        for i in range(0, 3):
            if checkboxes[i] == 'on':
                #Set current_timetable to the timetable picked
                current_timetable = generator.options[i]
                #Checks to see if there already is timetable linked to user id
                timetable = Timetable.query.filter_by(user_id=current_user.id).first()
                #If there isn't then add timetable to table
                if(timetable == None):
                    #Add this timetable to the database with the current user id as a foreign key
                    new_timetable = Timetable(data=current_timetable, user_id=current_user.id)
                    db.session.add(new_timetable)
                #If there is replace old timetable with new generated timetable
                else:
                    timetable.data = current_timetable
                #Commit changes to the database
                db.session.commit()
                
                #Clear all global variables so they can be used again when another revision timetable is generated
                generator_values.subjects = []
                generator.options = []
                generator.timetables = []
                generator.subject_blocks = []
                #Redirect to the home page with the current_timetable as the argument
                return redirect(url_for('views.home', timetable = current_timetable))


    return render_template("selection.html", options = generator.options)

#Function takes in email and checks if it is valid
def ValidateEmail(email):
    is_valid = True
    has_length = True
    #Searches for email in database to see if anyone has the same email
    user_email = User.query.filter_by(email=email).first()
    #If the same email is found in the database the user is told the email is already registered
    if user_email:
        flash('Email already registered', category='error')
        is_valid = False
    #If email is less than or equal to 4 characters, user is given pop up
    if len(email) <= 4: 
        flash('Email must be more than 4 characters', category="error")
        has_length = False
    
    #If email satisfies all conditions it is valid and function returns true
    return (is_valid and has_length)

#Function takes in username and checks if it is valid
def ValidateUsername(username):
    is_valid = True
    has_length = True
    #Searches for username in database to see if anyone has the same username
    user_username = User.query.filter_by(username=username).first()
    #If the same username is found in the database the user is told the username is taken
    if user_username:
        flash('Username already taken', category='error')
        is_valid = False
    #If the username is not between 8 and 20 characters it is not valid
    if len(username) < 7 or len(username) > 20:
        flash('Username must be between 8 and 20 characters', category='error')
        has_length = False
        
    
    #If username satisfies all conditions it is valid and function returns true
    return (is_valid and has_length)


#Checks whether password meets all conditions 
def ValidatePassword(password1, password2):
    specials = '`~!@#$%^&*()_-+={[]}|\:;<,>.?/'
    
    is_same = False
    has_length = False
    has_capital = False
    has_number = False
    has_special = False
    for char in password1:
        if char.isupper():
            has_capital = True
        if char.isdigit():
            has_number = True
        if char in specials:
            has_special = True
    
    #If password does not satisfy a condition the user will be told by a message pop up

    if password1 == password2:
        is_same =  True

    else:
        is_same = False
        flash('Passwords must match.', category='error')

    if len(password1) < 7 or len(password1) > 20:
        has_length = False
        flash('Password must be between 8 and 20 characters.', category="error")
    else:
        has_length = True

    if has_capital == False:
        flash('Password must have capital letter.', category="error")
        
    if has_number == False:
        flash('Password must have number.', category="error")
        
    if has_special == False:
        flash('Password must have special character.', category="error")
        
    #if all conditions are true then password is valid and return false, if not return false
    return (is_same and has_length and has_capital and has_number and has_special)
