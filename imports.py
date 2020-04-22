import csv
import os
from flask import Flask,render_template, request
from schema import *
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main(): 
    f = open("books.csv")
    reader = csv.reader(f) 
    next(reader, None)
    # try:
    #     db.execute("CREATE TABLE BOOKS (ISBN VARCHAR PRIMARY KEY, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year VARCHAR NOT NULL)")
    # except Exception as e:
    #     print(e)
    counter = 0
    for isbn, title, author, year in reader:
        counter += 1
        try:
            book = Book(isbn = isbn, title = title, author = author, year = year)
            db.session.add(book)
            print(isbn, counter, "in try")
        except:
            print(isbn, counter)
            continue
    db.session.commit()

if __name__ == "__main__": 
    with app.app_context():
        main()


