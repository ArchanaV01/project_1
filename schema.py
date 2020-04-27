from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import ForeignKey,PrimaryKeyConstraint

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "USERS"
    name = db.Column(db.String, primary_key = True)
    password = db.Column(db.String, nullable = False)
    created_at = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)

class Book(db.Model):
    __tablename__ = "BOOKS"
    isbn = db.Column(db.String, primary_key = True)
    title = db.Column(db.String, nullable = False)
    author = db.Column(db.String, nullable = False)
    year = db.Column(db.String, nullable = False)

class Review(db.Model):
    __tablename__ = "REVIEWS"
    isbn = db.Column(db.String, ForeignKey("BOOKS.isbn"))
    name = db.Column(db.String, ForeignKey("USERS.name"))
    review = db.Column(db.String)
    rating = db.Column(db.Integer)
    createTime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (PrimaryKeyConstraint('isbn', 'name'),)

