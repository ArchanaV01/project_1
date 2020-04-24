import os
import re
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
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
        pHash = generate_password_hash(password,"sha256")
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
        if (user == None or not check_password_hash(user.password,password)):
            error = "Invalid credentials"
            return render_template('register.html', error=error)
        else:
            session['logged_in'] = True
            session["USERNAME"] = user.name
            return render_template('user_home.html', name=user.name)
    # redirecting to register page if /auth is directly accessed
    if request.method == "GET":
        return render_template('register.html')


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if request.method == "POST":
        session.pop("USERNAME", None)
        session.pop("logged_in", None)
        return render_template("register.html")
            

@app.route("/book_page/<isbn>",methods=["GET","POST"])
def book_page(isbn):
    if request.method == "GET":
        #checking if user session is already present, if not redirecting to login page
        if not 'USERNAME' in session:
            return render_template("register.html", msg="Please login first")
        bookDetails = Book.query.get(isbn)
        #checking if the isbn is valid or not
        if bookDetails is None:
            return render_template("user_home.html", msg = "Invalid ISBN number")
        #redirecting to the bookpage with the reviews and bookdetails
        reviews = Review.query.filter_by(isbn=isbn).order_by(Review.createTime.desc()).all()
        return  render_template("book_page.html", bookDetails = bookDetails, reviews=reviews)


@app.route("/search")
def search():
    return render_template("user_home.html")

