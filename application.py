import os
import re

from flask import Flask, session, render_template, request, redirect
from schema import *
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html", name="")
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        # checking for empty credentials
        if (name == "" or password == ""):
            error = 'Invalid credentials'
            return render_template('register.html', error=error, name="")
        # checking for password strength
        if not isStrong(password):
            error = 'Weak Password'
            return render_template('register.html', error=error, name="")
        print(name, "  ", password)
        return render_template("register.html", name=name)


def isStrong(password):
    '''Checks the password strength'''
    if (len(password) < 6):
        return False
    elif not re.search("[a-z]", password):
        return False
    elif not re.search("[A-Z]", password):
        return False
    elif not re.search("[0-9]", password):
        return False
    elif not re.search("[_@$]", password):
        return False
    else:
        return True
