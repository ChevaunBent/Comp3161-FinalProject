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

#Generates Tables from sql file
with conn.connect() as con:
    file = open('app/static/SQL/sqlfile.sql')
    query = text(file.read())
    con.execute(query)
    con.close()

###
# Routing for application.
###

#Used to add a new user to the system
@app.route("/register", methods=['POST', 'GET'])
def register():
    # Instantiate form class
    userform = CreateUser()
    #Validates form data
    if request.method == "POST" and userform.validate_on_submit():
        #Gets data from form
        firstname = userform.firstname.data
        lastname = userform.lastname.data
        age = userform.age.data
        email = userform.email.data
        telephone = userform.telephone.data
        preference = userform.preference.data
        username = userform.username.data
        password = userform.password.data
        confirm = userform.confirm.data
        secure_password = sha256_crypt.encrypt(str('password'))
        #Creates a database object by binding the connection created earlier
        db = scoped_session(sessionmaker(bind=conn))
        #Query Server database using database object
        usernamedata = db.execute("SELECT username FROM users WHERE username=:username", {
                                  "username": username}).fetchone()
        #Generates a random user ID to be used in database
        userid = genId(firstname, lastname)
        #Process Results from database
        if usernamedata != None: 
            flash("Username already taken please try another username","danger")
            return render_template('register.html', form = userform)
        #If username is not in database then create user using data entered in form
        if usernamedata == None and password == confirm:
            #Database Transaction Management
            try:
                db.execute("INSERT INTO users(userid,firstname,lastname,age,email,telephone,preference,username,password)VALUES(:userid,:firstname,:lastname,:age,:email,:telephone,:preference,:username,:password)",
                           {"userid":userid,"firstname": firstname, "lastname": lastname, "age":age, "email":email, "telephone": telephone, "preference": preference, "username": username, "password": secure_password})
                db.commit()
                flash("registration successful", "success")
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
    form = LoginForm()
    #Validates form data
    if request.method == "POST" and form.validate_on_submit():
        #Gets data from form
        username = form.username.data
        password = form.password.data
        #Creates a database object by binding the connection created earlier at startup
        db = scoped_session(sessionmaker(bind=conn))
        #Querying the server using database object
        usernamedata = db.execute("SELECT username FROM users WHERE username=:username", {
                                  "username": username}).fetchone()
        passworddata = db.execute("SELECT password FROM users WHERE username=:username", {
                                  "username": username}).fetchone()
        useriddata = db.execute("SELECT userid FROM users WHERE username=:username", {
                                  "username": username}).fetchone()
        pw = passworddata[0]
        usr = usernamedata[0]
        usrid = useriddata[0]
        #Processing results of query
        if usr is None:
            #Informs user no such user exists
            flash("No such user exists", "danger")
            return render_template('login.html', form = form)
        else:
            #If username exists, check password entered agaianst password stored in database for that user
            if sha256_crypt.verify(password,pw):
                #If credentials match, create a sesstion and log in 
                session['username']=list(usr)
                session['userid']=int(usrid)
                #Indicate to user that they have logged in
                flash("You are now logged in!", "success")
                #redirects user to a secured page that can only be accessed after loggin in
                #Only for demonstration Purposes
                return redirect(url_for('secured'))
            else:
                #if Credentials are incorrect, promt user to try entering again
                flash("Incorrect password entered please try again", "danger")
                return render_template('login.html', form = form)
        #In the event authication fails completely for unknown reason to user, ask them to try again
        flash("An Error Occured please try logging in again, if error persists, contact administrator", "danger")
    return render_template('login.html', form = form)    

#Route used for logging a user out of the
@app.route("/logout")
def logout():
    #Remove active session
    session.pop('username', None)
    session.pop('userid', None)
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
    if request.method == "POST" and userform.validate_on_submit():
        #Gets data from form
        title = userform.title.data
        instructions = userform.instructions.data
        # Get Photo of recipe and save to uploads folder
        userfile = request.files['upload']
        filename = secure_filename(userfile.filename)
        userfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #Gets session data on the current logged in user
        username = str(session['username'])
        UID = (session['userid'])

        #Generate recipeID and receive date created from Adds Table
        RID = genId(title, filename)
        #Creates a database object by binding the connection created earlier
        db = scoped_session(sessionmaker(bind=conn))
        if UID != None:
            try:
                db.execute("INSERT INTO recipes(recipeid,title,instructions,filename)VALUES(:recipeid,:title,:instructions,:filename)",
                       {"recipeid":RID,"title": title,"instructions": instructions, "filename":filename})
                db.commit()
                Adds(UID, RID)
                flash("Recipe Added Successfully", "success")
                return redirect(url_for('recipes'))
            except Exception as error:
                flash("Failed to update record to database, rollback done, try adding again" "danger")
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

#Route used to display about page
@app.route('/secured/')
def secured():
    """Render the website's about page."""
    return render_template('secured.html')

#Route used to display secured page
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
    recipes = db.execute("SELECT * FROM recipes").fetchall()
    #Handles our GET request
    if request.method == "GET":
        """Render the website's recipes page."""
        return render_template('recipes.html', recipes = recipes)
    #Handles our POST request despite there should not be a post request for this route
    elif request.method == "POST":
        response = make_response(jsonify(recipes))                                           
        response.headers['Content-Type'] = 'application/json'            
        return response

# Used to generate a file's url for display
@app.route("/uploads/<filename>")
def get_image(filename):
    rootdir = os.getcwd()
    return send_from_directory(rootdir + "/" + app.config['UPLOAD_FOLDER'],
                               filename)

#Route for finding and displaying a specific recipe that was selected
@app.route('/recipe/<recipeid>', methods=["GET", "POST"])
def get_recipe(recipeid):
    #Get a specific recipe in the database using the recipe ID that was generated on insertion
    db = scoped_session(sessionmaker(bind=conn))
    #Queries the database using database object for all recipes
    recipe = db.execute("SELECT * FROM recipes WHERE recipeid=:recipeid", {
                                  "recipeid": recipeid}).fetchone()
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
