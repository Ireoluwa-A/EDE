from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from flask_mysqldb import MySQL
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import random
from helpers import apology, login_required
import pyodbc 

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                    'Server=(LocalDB)\MSSQLLocalDB;'
                    #   'Server=DESKTOP-55O8CAH\LOCALDB#43D00389;'
                      'Database=EDE;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()


# Old configuration to sql server
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


    cursor.execute('''SELECT * FROM users ''')
    results = cursor.fetchall()
    print(results)
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

            # Print passwords to see in terminal
            print(f"username is: {username}")
            print(f"password is: {password}")
            print(f"Hashed password is: {hashPass}")
            print(f"language is: {language}")

            # Open up database and set cursor  
            cur = mysql.connection.cursor()          
            cur.execute("SELECT * FROM user WHERE username = %s", [username] )
            matchingUsernames = cur.fetchall()
            print(matchingUsernames)
            # Check if username already exists in database  
            if len(matchingUsernames) != 0: # If length isn't zero then a match exists in database
                return apology("Username already exists", 403)
    
            else:
            # Getting this far means valid inputs have been given
                cur = mysql.connection.cursor()  
                # Insert their details into database
                cur.execute("INSERT INTO user (username, hash, language) VALUES (%s, %s, %s)", [username, hashPass, language])
                mysql.connection.commit()
                print("Inserted user into database")

                # Log them in
                session.clear()
                cur2 = mysql.connection.cursor()  
                cur2.execute("SELECT id FROM user WHERE username = %s", [username])  # Query database for id
                rows = cur2.fetchall()
                print(rows)
                # Remember which user has logged in
                session["user_id"] = rows[0]["id"]
                return redirect("/info")

        # Page was requested via GET
        else:
            # cursor2 = conn.cursor()
            # cursor2.execute("INSERT INTO users (name, hash, language) VALUES ('ire', 'hash', 'French')")
            # cursor2.commit()
            # print("second time:")

            return render_template("signup.html")




@app.route("/login", methods=["GET", "POST"])
def login():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Forget any user_id
        session.clear()
        # Define common variables
        username = request.form.get("username")
        password = request.form.get("password") 

        # Ensure fields arent blank
        if not username:
            return apology("must provide username", 403)
        elif not password:
            return apology("must provide password", 403)

        # Query database for username
        cur = mysql.connection.cursor()          
        cur.execute("SELECT * FROM user WHERE username = %s", [username] )
        rows = cur.fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)
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

    cur = mysql.connection.cursor()          
    cur.execute("SELECT * FROM user WHERE id= %s", [currentUser] )
    rows = cur.fetchall()

    name = rows[0]['username']
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
    randomTip = random.randint(0,9)  # means we have 10 tips.

    # Pass all this information to table html
    return render_template("table.html",name=name,language=language,greeting=greeting,randomTip=randomTip)

    # return render_template("table.html",name=name,language=language,firstTime=firstTime,intensity=intensity,wakeup=wakeup,sleep=sleep,randomTip=randomTip,access=access)




# Gathers info on user. Only runs when users signs up.
@app.route("/info", methods=["GET", "POST"])
def info():
    # Common variables
    currentUser=session["user_id"]
    cur = mysql.connection.cursor()  
    cur.execute("SELECT username, language FROM users WHERE id = %s", [currentUser])
    rows = cur.fetchall()
    username = rows[0]['username']
    language = rows[0]['language']

    # Insert the info they've given us
    if request.method == "POST":

        # Get all information from fields:
        intensity = request.form.get("intensity")
        goals = request.form.get("goals")   
        access = request.form.get("access")   
        time = request.form.get("time")
        print(intensity)
        print(goals)
        print(access)
        print(time)
        
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
        cur2 = mysql.connection.cursor()          
        cur2.execute("SELECT first_time FROM info WHERE user_id = %s", [username] )
        firstTimeRows = cur2.fetchall()

        # If they dont have a first time, it means its actually their first time
        if not firstTimeRows:

            # Insert into the table all this information
            cur3 = mysql.connection.cursor() 
            cur3.execute("INSERT INTO info (user_id, intensity, goals, media_access, time) VALUES (%s,%s,%s,%s,%s)",
                        [currentUser, intensity, goals, access, time] )
            mysql.connection.commit()

        else:
        # Means they've been here before and are trying to update preferences
            cur4 = mysql.connection.cursor() 
            cur4.execute("UPDATE info SET (intensity, goals, media_access, time) = (%s,%s,%s,%s,%s) WHERE user_id = %s",
                        [intensity, goals, access, time, currentUser] )
            mysql.connection.commit()

        # Go back to table so we can use the information there
        return redirect('/table')

    else:
        # Means they just want the form.
        return render_template("info.html",language=language)





@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    return redirect("/")
