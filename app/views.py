import os, random, datetime
import random
from flask import Flask, render_template, url_for, request, session, logging, redirect, flash
from flask import send_from_directory, abort, jsonify, make_response
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename
from app import app
from app.forms import LoginForm, CreateUser, UploadForm
import pandas as pd
from faker import Faker


# Sets up connections to database using database settings stored in environment variable
conn = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

###
# Routing for application.
###

#If a user is logged in already they wont be allowed to register
@app.route("/register_logged")
def register_logged():
    return redirect(url_for('login'))


#Used to add a new user to the system
@app.route("/register", methods=['POST', 'GET'])
def register():
    #session.pop('csrf_token', None)
    # Instantiate form class
    userform = CreateUser()
    #Validates form data
    if request.method == "POST" :
        #Gets data from form
        firstname = userform.firstname.data
        lastname = userform.lastname.data
        age = userform.age.data
        height = userform.height.data
        weight = userform.weight.data
        password = userform.password.data
        confirm = userform.confirm.data
        secure_password = sha256_crypt.hash(str(password))
        #Creates a database object by binding the connection created earlier
        db = scoped_session(sessionmaker(bind=conn))
        #Generate personID
        PID = genId("person")
        #Process Results from database
        if password == confirm: 
            #Database Transaction Management
            try:
                db.execute("INSERT INTO person(person_id,first_name,last_name,age,height,weight,password)VALUES(:person_id,:first_name,:last_name,:age,:height,:weight,:password)",
                           {"person_id":PID,"first_name": firstname, "last_name": lastname, "age":age, "height":height, "weight":weight, "password": secure_password})
                db.commit()
                flash("Registration Successful Please login", "success")
                return redirect(url_for('login'))
            except Exception as error:
                flash("Failed to update record to database, rollback done, try adding again" "danger")
                print("Failed to update record to database, rollback done: {}".format(error))
                # reverting changes if exception occurs
                db.rollback()
            finally:
                # closing created database object .
                if conn:
                    db.remove()
        #if password and conform password field doesnt match an error is displayed
        flash("Password and confirm password do not match","danger")
        return render_template('register.html', form = userform)
    #If form validation fails, errors are displayed on form 
    flash_errors(userform)
    return render_template('register.html', form = userform)

#Route used to log a user into the system
@app.route("/login", methods=['POST', 'GET'])
def login():
    #instantiate LoginForm
    logform = LoginForm()
    #Validates form data
    if request.method == "POST" and logform.validate_on_submit():
        #Gets data from form
        username = logform.username.data
        password = logform.password.data
        #seperates username to get ID
        try:
            #Handles possible exception from bad username input
            txt = username.split('_')
            user= txt[0]
            userid = int(txt[1])
        except Exception as error:
                flash("Incorrect Username Format, try logging in again. Format: FirstName_ID", "danger")
                return render_template('login.html', form = logform)
        #Creates a database object by binding the connection created earlier at startup
        db = scoped_session(sessionmaker(bind=conn))
        #Querying the server using database object
        usernamedata = db.execute("SELECT first_name FROM person WHERE person_id=:person_id", {
                                  "person_id": userid}).fetchone()
        passworddata = db.execute("SELECT password FROM person WHERE person_id=:person_id", {
                                  "person_id": userid}).fetchone()
        useriddata = db.execute("SELECT person_id FROM person WHERE person_id=:person_id", {
                                  "person_id": userid}).fetchone()
        #Processing results of query
        if usernamedata is None:
            #Informs user no such user exists
            flash("No such user exists", "danger")
            return render_template('login.html', form = logform)
        else:
            pw = passworddata[0]
            usr = usernamedata[0]
            usrid = useriddata[0]
            #If username exists, check password entered agaianst password stored in database for that user
            if sha256_crypt.verify(password,pw):
                #If credentials match, create a sesstion and log in 
                session['username']=str(usr)
                session['userid']=int(usrid)
                #Indicate to user that they have logged in
                flash("You are now logged in!", "success")
                #redirects user to a secured page that can only be accessed after loggin in
                #Only for demonstration Purposes
                return redirect(url_for('secured'))
            else:
                #if Credentials are incorrect, promt user to try entering again
                flash("Incorrect password entered please try again", "danger")
                return render_template('login.html', form = logform)
        #In the event authication fails completely for unknown reason to user, ask them to try again
        flash("An Error Occured please try logging in again, if error persists, contact administrator", "danger")
    return render_template('login.html', form = logform)    

#Route used for logging a user out of the
@app.route("/logout")
def logout():
    #Remove active session
    session.pop('username', None)
    session.pop('userid', None)
    session.pop('csrf_token', None)
    session.clear()
    #Notify Log out and redirect to home page
    flash("You have been succcessfully logged out", "success")  
    return render_template('home.html')

#Route used for adding a recipe
@app.route("/addrecipe", methods=['POST', 'GET'])
def addrecipe():
    # Instantiate form class
    userform = UploadForm()
    #Validates form data
    if request.method == "POST" and userform.validate_on_submit:
        #Gets data from form
        name = userform.name.data
        serving = userform.servings.data
        nutrition_no = userform.nutrition_no.data
        calories = userform.calories.data
        total_fat = userform.total_fat.data
        sugar = userform.sugar.data
        sodium = userform.sodium.data
        protein = userform.protein.data
        saturated_fat = userform.saturated_fat.data
        instructions = userform.instructions.data
        #Gets session data on the current logged in user
        '''username = str(session['username'])'''
        UID = str(session['userid'])

        #Generate recipeID and receive date created from Adds Table
        RID = genId("recipe")
        imgID = str(RID)

        # Get Photo of recipe and save to uploads folder
        userfile = request.files['upload']
        filename = secure_filename(userfile.filename)
        userfile.save(os.path.join(app.config['UPLOAD_FOLDER'], imgID))

        #Creates a database object by binding the connection created earlier
        db = scoped_session(sessionmaker(bind=conn))
        if UID != None:
            try:
                db.execute("INSERT INTO nutrition(nutrition_no,calories,total_fat,sugar,sodium,protein,saturated_fat)VALUES(:nutrition_no,:calories,:total_fat,:sugar,:sodium,:protein,:saturated_fat)",
                       {"nutrition_no":nutrition_no,"calories": calories,"total_fat": total_fat, "sugar":sugar,"sodium":sodium,"protein":protein,"saturated_fat":saturated_fat})
                db.execute("INSERT INTO recipe(recipe_id,name,serving,nutrition_no)VALUES(:recipe_id,:name,:serving,:nutrition_no)",
                       {"recipe_id":RID,"name": name,"serving": serving, "nutrition_no":nutrition_no})
                db.commit()
                flash("Recipe Added Successfully", "success")
                return redirect(url_for('recipes'))
            except Exception as error:
                flash("Failed to update record to database, rollback done, try adding again", "danger")
                print("Failed to update record to database, rollback done: {}".format(error))
                # reverting changes if exception occurs
                db.rollback()
            finally:
                # closing created database object .
                if conn:
                    db.remove()
    #If form validation fails, errors are displayed on form 
    flash_errors(userform)
    return render_template('newrecipe.html', form = userform)

#Route used for displaying home page
@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

#Route used to display secured page
@app.route('/secured/')
def secured():
    """Render the website's about page."""
    return render_template('secured.html')

#Route used to display about page
@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

#Route for displaying all recipes
@app.route('/recipes/', methods=["GET", "POST"])
def recipes():
    #Creates a database object by binding the connection created earlier
    db = scoped_session(sessionmaker(bind=conn))
    #Queries the database using database object for all recipes
    res = db.execute("SELECT * FROM recipe").fetchall()
    recipes = list(res)
    #Handles our GET request
    if request.method == "GET":
        """Render the website's recipes page."""
        return render_template('recipes.html', recipes = recipes)
    #Handles our POST request despite there should not be a post request for this route
    elif request.method == "POST":
        response = make_response(jsonify(recipes))                                           
        response.headers['Content-Type'] = 'application/json'            
        return response

@app.route('/meal')
def meal():
    """Render the website's about page."""
    return render_template('dummy.html')

# Used to generate a file's url for display
@app.route("/uploads/<filename>")
def get_image(filename):
    rootdir = os.getcwd()
    return send_from_directory(rootdir + "/" + app.config['UPLOAD_FOLDER'],
                               filename)

#Route for finding and displaying a specific recipe that was selected
@app.route('/recipe/<recipe_id>', methods=["GET", "POST"])
def get_recipe(recipe_id):
    #Get a specific recipe in the database using the recipe ID that was generated on insertion
    db = scoped_session(sessionmaker(bind=conn))
    #Queries the database using database object for all recipes
    recipe = db.execute("SELECT * FROM recipe WHERE recipe_id=:recipe_id", {
                                  "recipe_id": recipe_id}).fetchone()
    #Handles our Get request to fetch a recipe that mathces the recipe ID
    if request.method == "GET":
        return render_template("viewrecipe.html", recipe=recipe)
    
    #Handles a POST request for in the event a POST request is generated despite this should not happen
    elif request.method == "POST":
    #Creates an object representation of our POST request
        if recipe is not None:
            response = make_response(jsonify(id = recipe[0], title = recipe[1], instructions = recipe[2], 
            upload = recipe[3]))
            response.headers['Content-Type'] = 'application/json'            
            return response
        else:
            flash('Recipe Not Found', 'danger')
            return redirect(url_for("recipes"))

#Generates the next ID to assign on manual input from the front end
def genId(table):
    #Get a specific recipe in the database using the recipe ID that was generated on insertion
    db = scoped_session(sessionmaker(bind=conn))
    #Queries the database using database object for all recipes
    currentcount = db.execute("SELECT COUNT(*) FROM "+ table)
    userid = list(currentcount)[0][0] + 1
    return int(userid)

     

"""
#No longer using
# Generates a unique 5 digit ID for each entry in our database
def genId(title, filename):
    id = []
    for x in title:
        id.append(str(ord(x)))
    for x in filename:
        id.append(str(ord(x)))
    random.shuffle(id)
    res = ''.join(id)
    return int(res[:5])
"""

#Helper function that populates Adds table and get a date created value
def Adds(UID,RID):
    if UID != None and RID != None:
        date_created = datetime.date.today()
        #Creates a database object by binding the connection created earlier
        db = scoped_session(sessionmaker(bind=conn))
        #Database Transaction Management
        try:
            db.execute("INSERT INTO adds(userid,recipeid,datecreated)VALUES(:userid,:recipeid,:datecreated)",
                           {"userid":UID,"recipeid": RID, "datecreated": date_created})
            db.commit()
            #if successful then creation date is submitted
            return date_created
        except Exception as error:
            flash("Failed to update record to database, rollback done, try adding again", "danger")
            print("Failed to update record to database, rollback done: {}".format(error))
            # reverting changes if exception occurs
            db.rollback()
        finally:
            # closing created database object .
            if conn:
                db.remove()
    #if error occured during updating of table, None will be returned 
    return None

#Used to flash errors on a form
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


###
# The functions below should be applicable to all Flask apps DO NOT EDIT.
###
@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
