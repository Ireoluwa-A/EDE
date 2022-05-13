import os
from pip._vendor import requests
import urllib.parse

from flask import redirect, render_template, request, session, escape
from functools import wraps

def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", top=code, bottom=escape(message))


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Turns cursor data into a dict so we can index into it
def makeDict(cursor):
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():  
            results.append(dict(zip(columns, row)))
        return results
