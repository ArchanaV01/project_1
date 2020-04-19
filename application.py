import os
import re
from datetime import datetime

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

@app.route("/admin")
def admin():
    users = User.query.all()
    return render_template("admin.html", list = users)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html", name="")
    if request.method == "POST":
        if (request.form('logout_button') == 'logout_now'):
            session.pop("USERNAME", None)
            session.pop("logged_in", None)
            return render_template("register.html", name="")
        name = request.form.get("name")
        password = request.form.get("password")
        # checking for empty credentials
        if (name == "" or password == ""):
            error = 'Empty credentials'
            return render_template('register.html', error=error, name="")
        # checking for password strength
        if not isStrong(password):
            error = 'Weak Password'
            return render_template('register.html', error=error, name="")
        print(name, "  ", password)
        user = User(name = name, password = password)
        db.session.add(user)
        db.session.commit()
        print("printing the database")
        users = User.query.all()
        for user in users:
            print(user.name, user.password, user.created_at)
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

@app.route("/auth", methods=["POST", "GET"])
def is_authorised():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        # checking for empty credentials
        if (name == "" or password == ""):
            error = 'Empty credentials'
            return render_template('register.html', error=error, name="")
        user = User.query.get(name)
        if (user == None or user.password != password):
            error = "Invalid credentials"
            return render_template('register.html', error=error, name="")
        else:
            session['logged_in'] = True
            session["USERNAME"] = user
            return render_template('user_home.html', name = user.name)
    if request.method == "GET":
        return render_template('register.html',name = "") 