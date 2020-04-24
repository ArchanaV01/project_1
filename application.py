import os
import re
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, session, render_template, request, redirect
from schema import *
from sqlalchemy import or_
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
    users = User.query.order_by(User.created_at.desc())
    return render_template("admin.html", list=users)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        print(name, "  ", password)

        # checking for already existing user
        user = User.query.get(name)
        print(user)
        if user != None:
            print("existing user")
            error = "Already Existing User"
            return render_template("register.html", error=error)

        # checking for empty credentials
        if (name == "" or password == ""):
            error = 'Empty credentials'
            return render_template('register.html', error=error)

        # checking for password strength
        if not isStrong(password):
            error = 'Weak Password'
            return render_template('register.html', error=error)

        # checked all the possible errors, finally adding the user
        pHash = generate_password_hash(password, "sha256")
        user = User(name=name, password=pHash)
        db.session.add(user)
        db.session.commit()
        return render_template("register.html", name=name)


def isStrong(password):
    '''Checks the password strength'''
    if (len(password) < 8):
        return False
    elif not re.search("[a-z]", password):
        return False
    elif not re.search("[A-Z]", password):
        return False
    elif not re.search("[0-9]", password):
        return False
    elif not re.search("[!@#$%^&*]", password):
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
            return render_template('register.html', error=error)

        # checking if regsitered and if so checking the password
        user = User.query.get(name)
        if (user == None or not check_password_hash(user.password, password)):
            error = "Invalid credentials"
            return render_template('register.html', error=error)
        else:
            session['logged_in'] = True
            session["USERNAME"] = user
            return render_template('user_home.html', name=user.name)
    # redirecting to register page if /auth is directly accessed
    if request.method == "GET":
        return render_template('register.html')


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if request.method == "POST":
        if (request.form('logout_button') == 'logout_now'):
            session.pop("USERNAME", None)
            session.pop("logged_in", None)
            return render_template("register.html")


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        keyWord = request.form.get("key")
        attribute = request.form.get("category")
        print(keyWord, attribute)
        return render_template("user_home.html", list=get_books(keyWord, attribute))
    if request.method == "GET":
        # keyWord = request.key
        print(request)
        return render_template("user_home.html")


def get_books(key, attribute):
    if attribute == "Title":
        print('in title')
        books = Book.query.filter(or_(Book.title.like("%{}%".format(key)))).all()
    elif attribute == "Author":
        print('in author')
        books = Book.query.filter(or_(Book.author.like("%{}%".format(key)))).all()
    elif attribute == "Year":
        print('in year')
        books = Book.query.filter(or_(Book.year.like("%{}%".format(key)))).all()
    else:
        print('in else')
        books = Book.query.filter(or_(Book.title.like(
            "%{}%".format(key)), Book.author.like("%{}%".format(key)), Book.year.like("%{}%".format(key)))).all()
    print(len(books))
    return books