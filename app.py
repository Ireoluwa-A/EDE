from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from flask_mysqldb import MySQL
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import random
import MySQLdb
from helpers import apology, login_required, makeDict
import pyodbc
import mysql.connector 

import urllib.parse 
from flask_sqlalchemy import SQLAlchemy



# Configure Database URI: 
params = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=localhost;DATABASE=EDE;UID=sa;PWD=Strong.Pwd-123")


# initialization
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'supersecret'
# app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# # extensions
# db = SQLAlchemy(app)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# conn_str = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
#                     'Server=localhost;'
#                     #'Server=DESKTOP-55O8CAH\LOCALDB#43D00389;'
#                       'Database=EDE;'
#                       'UID=sa;'
#                       'PWD=Strong.Pwd-123;')
# conn = pyodbc.connect(conn_str)                  

# conn = mysql.connector.connect(host='localhost',
#                         user='root',
#                         password='Strong.Pwd-123', 
#                         db='EDE')

# conn = MySQLdb.Connect(host="0.0.0.0", port=1433,user="sa", passwd="Strong.Pwd-123", db="EDE")

# app.config['MYSQL_USER'] = 'sql9360415'
# app.config['MYSQL_PASSWORD'] = '8W1QzCE6qN'
# app.config['MYSQL_HOST'] = 'sql9.freemysqlhosting.net'
# app.config['MYSQL_DB'] = 'sql9360415'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# mysql = MySQL(app)
# mysql = conn.cursor()

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response




@app.route("/")
def index():
    # Query for creating table and inserting into it

    # cur.execute('''CREATE TABLE user (id INTEGER, username VARCHAR(20), hash TEXT, language TEXT )''')
    # cur.execute('''INSERT INTO user (username, hash, language) VALUES ('ire', 'random', 'French')''')
    # mysql.connection.commit()
    # cur.execute('''SELECT * FROM user ''')
    # results = cur.fetchall()
    # print(results)

    # To print entire table

    # cur = mysql.connection.cursor()  
    # cur.execute("SELECT * FROM user")
    # test = cur.fetchall()
    # print(test)
    # mysql.connection.commit()


    # db.execute("SELECT * FROM users")
    # print(db.execute("SELECT * FROM users"))
    print("EXECUTED")
    # Turn our results into a dict so we can index into it nicely
    # results = makeDict(cursor)

    # results = makeDict(cursor, "id name hash language")
    # results = cursor.fetchall()
    # print(results)
    # cursor.close()
    # print(cursor)
    return render_template("index.html")



@app.route("/signup", methods=["GET", "POST"])
def signup():

    # They want to sign up
    if request.method == "POST": 

    # Error checks

        # Define common variables:
        username = request.form.get("username").lower()
        password = request.form.get("password")
        confirmPassword = request.form.get("confirmPassword")
        hashPass = generate_password_hash(password)
        language = request.form.get("language")

        # Ensure username, password and confirm password field are completed.
        # This will be done in java too, but good to have extra backup checks.
        if not username:
            return apology("must provide username", 403)
        elif not password:
            return apology("must provide password", 403)
        elif not confirmPassword:
            return apology("Must confirm password", 403)
        elif not language:
            return apology("Must provide a language to learn")
        elif password != confirmPassword:  # Checks if confirmed password is the same as original
            return apology("Passwords must be the same", 403)

        # Print info to see in terminal
        print(f"username is: {username}")
        print(f"password is: {password}")
        print(f"Hashed password is: {hashPass}")
        print(f"language is: {language}")

        # Open up database and set cursor  
        cursor = conn.cursor()       
        cursor.execute("SELECT * FROM users WHERE name = ?", username)
        matchingUsernames = makeDict(cursor)
        cursor.close()

        # Check if username already exists in database  
        if len(matchingUsernames) != 0: # If length isn't zero then a match exists in database
            return apology("Username already exists", 403)

        else:
        # Getting this far means valid inputs have been given
            cursor2 = conn.cursor()
                # Insert their details into database
            cursor2.execute("INSERT INTO users (name, hash, language) VALUES (?, ?, ?)", username, hashPass, language)
            cursor2.commit()
            cursor2.close()
            print("Inserted user into database")

            # Log them in
            session.clear()
            cursor3 = conn.cursor()
            cursor3.execute("SELECT id FROM users WHERE name = ?", username)  # Query database for id
            rows = makeDict(cursor3)
            cursor3.close()
            
            userID = rows[0]['id']
            print(f"successfully signed up {username}, id: {userID}")
            # Remember which user has logged in
            session["user_id"] = userID
            return redirect("/info")

    # Page was requested via GET
    else:
        return render_template("signup.html")




@app.route("/login", methods=["GET", "POST"])
def login():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Forget any user_id
        session.clear()

        # Define common variables
        name = request.form.get("username")
        password = request.form.get("password") 

        # Ensure fields arent blank
        if not name:
            return apology("must provide username", 403)
        elif not password:
            return apology("must provide password", 403)

        # Query database for username
        cursor = conn.cursor()         
        cursor.execute("SELECT id,name,hash FROM users WHERE name = ?", name )
        rows = makeDict(cursor)
        cursor.close()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]['hash'], password):
            return apology("Invalid username and/or password", 403)
        print("Username found!")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to table page
        return redirect("/table")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route("/table")
@login_required
def table():
    # Get important variables on particular user
    currentUser = session["user_id"]
    cursor = conn.cursor() 
    cursor.execute("SELECT id, name, language FROM users WHERE id = ?", currentUser)    
    rows = makeDict(cursor)
    cursor.close() 

    nameCase = rows[0]['name']
    name = nameCase.capitalize()
    print(name)

    language = rows[0]['language']
    greeting = "Welcome back"
    
    # Check if its their first time so we can print generating table, and change it to zero(signifying its not their first)
    # infoRows = db.execute("SELECT * FROM info WHERE user_id = ?",currentUser)
    # firstTime = infoRows[0]["first_time"]
    # if firstTime == 1:
    #     revisiting = 0
    #     greeting = "Welcome"
    #     db.execute("UPDATE info SET first_time = :revisiting WHERE user_id = :currentUser",
    #                 revisiting=revisiting, currentUser=currentUser)

    print(f"{greeting} {name}. You're studying {language}")

    # Info needed to show the right table.
    # intensity = infoRows[0]['intensity']
    # print(intensity)
    # # To get the wakeup and sleep times
    # timesSpaces = infoRows[0]['time'] # There's a space inbetween the wakeup and sleeping time
    # # Split string to get individual wakeup and sleep times
    # times = timesSpaces.split()
    # wakeup = times[0]
    # sleep = times[1]
    # print(wakeup)
    # print(sleep)

    # access = infoRows[0]['media_access']
    # print(access)

    # Random tip for cycling through random tips that'll show up when clicking on table
    randomTip = random.randint(0,10)  # Means we have 11 tips.
    
    # Pass all this information to table html
    return render_template("table.html",name=name,language=language,greeting=greeting,randomTip=randomTip)




# Gathers info on user. Only runs when users signs up.
@app.route("/info", methods=["GET", "POST"])
def info():
    # Common variables
    currentUser=session["user_id"]
    cursor = conn.cursor()  
    cursor.execute("SELECT name, language FROM users WHERE id = ?", currentUser)
    rows = makeDict(cursor)
    language = rows[0]['language']

    # Insert the info they've given us
    if request.method == "POST":

        # Get all information from fields:
        intensity = request.form.get("intensity")
        goals = request.form.get("goals")   
        access = request.form.get("access")   
        time = request.form.get("time")
        print(f"Itensity is: {intensity}")
        print(f"Goals are: {goals}")
        print(f"Access is: {access}")
        print(f"Awake times are: {time}")
        
        # Error checks for if they somehow get past built in java script checks
        if not intensity:
            return apology("Must provide an intensity")
        elif not goals:
            return apology("Must provide goals")
        elif not access:
            return apology("Must provide an access to services value")
        elif not time:
            return apology("Must provide an approximate sleep and wake up time")

        # Check if its their first time so we can insert instead of update
        cursor = conn.cursor()           
        cursor.execute("SELECT first_time FROM info WHERE user_id = ?", currentUser)
        firstTimeRows = makeDict(cursor)
        cursor.close()

        # If they dont have a first time, it means its actually their first time
        if not firstTimeRows:

            # Insert into the table all this information
            cursor2 = conn.cursor() 
            cursor2.execute("INSERT INTO info (user_id, intensity, goals, media_access, time) VALUES (?,?,?,?,?)",
                            currentUser, intensity, goals, access, time )
            cursor2.commit()
            cursor2.close()

        else:
        # Means they've been here before and are trying to update preferences
            cursor3 = conn.cursor() 
            cursor3.execute("UPDATE info SET (intensity, goals, media_access, time) = (?,?,?,?) WHERE user_id = ?",
                            intensity, goals, access, time, currentUser)
            cursor3.commit()
            cursor3.close()

        # Go back to table so we can use the information there
        return redirect('/table')

    else:
        # Means they just want the form.
        return render_template("info.html",language=language)





@app.route("/editpreferences",methods=["GET", "POST"])
@login_required
def editpreferences():
# Will allow users to change data we put in info page.

    # This means they want to edit their preferences
    if request.method == "POST":
        # Make it so that the rest of the program treats it like its their first time
        firstTime = 1
        cursor = conn.cursor() 
        cursor.execute("UPDATE info SET first_time = :firstTime WHERE user_id = :currentUser", currentUser=session["user_id"] ,firstTime=firstTime)
        cursor.commit()
        cursor.close()
        return redirect("/info")
    
    else:
# Simply to display info on user
        # First display current info on user.
        currentUser = session["user_id"]
        cursor2 = conn.cursor() 
        cursor2.execute("SELECT username, language FROM users WHERE id = ?", currentUser)
        user = makeDict(cursor2)
        cursor2.close()
        cursor3 = conn.cursor() 
        cursor3.execute("SELECT * FROM info WHERE user_id = ?", currentUser)
        info = makeDict(cursor3)

        username = user[0]['username']
        language = user[0]['language']

        intensity = info[0]['intensity']
        goals = info[0]['goals']
        access = info[0]['media_access']

        timesSpaces = info[0]['time']
        times = timesSpaces.split()
        wakeup = times[0]
        sleep = times[1]

        # Pass it all to html
        return render_template("editpreferences.html",username=username, language=language, intensity=intensity, goals=goals, access=access, wakeup=wakeup, sleep=sleep)




# Forum of stories and stuff for language learners..
@app.route("/connectwithothers",methods=["GET", "POST"])
@login_required
def connectwithothers():

    currentUser = session["user_id"]

    # Meaning they're trying to post something to the forum board.
    if request.method == "POST":

        # Insert the chat into the database as well as the time and user who posted.
        newPost = request.form.get('post')
        if not newPost:
            return apology("must provide post")

        # Get the time of posting...
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_TIMESTAMP")
        timeRows = makeDict(cursor)

        # timeRows = db.execute("SELECT datetime('now','localtime')")
        # time=timeRows[0]["datetime('now','localtime')"]

        cursor.close()

        # Put info from post into database so as to show it displayed on the page.
        cursor = conn.cursor() 
        cursor.execute("INSERT INTO posts (user_id, post, time) VALUES (:currentUser, :post, :time)",
                    currentUser=currentUser, post=newPost, time=time)
        cursor.commit()
        cursor.close()
        # Refresh web page for him
        return redirect("/connectwithothers")

    # Means we need to show them all the posts(from the databasea)
    else:

    # Extract the posts form database and pass to html form.

        # Get the posts by the people and time
        cursor2 = conn.cursor() 
        cursor2.execute("SELECT post, time FROM posts")
        posts = makeDict(cursor2)
        cursor2.close()

        # Id of the poster so we can get their username
        cursor3 = conn.cursor()
        cursor3.execute("SELECT user_id FROM posts")
        posterID = makeDict(cursor3)
        cursor3.close()

        usernames = []
        for n in range(len(posterID)):
            # Append their actual usernames into a list. So this is essentially a list of a list of python dictionaries.
            # E.g [ [{'username': 'ire'}], [{'username': 'ire'}], [{'username': 'ire'}], [{'username': 'ire'}] ]
            cursor4 = conn.cursor()
            cursor4.execute("SELECT username FROM users WHERE id = ?", posterID[n]['user_id'])
            currentUsername = makeDict(cursor4)
            usernames.append(currentUsername)
            cursor4.close()

        noOfPosts = len(posts) # Get the number of posts so as to iterate

        # Pass information to html where we will display the forum and allow user to post stuff to it.
        return render_template("connectwithothers.html",posts=posts, noOfPosts=noOfPosts, usernames=usernames)




@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)