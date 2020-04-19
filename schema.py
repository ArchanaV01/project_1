from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "USERS"
    name = db.Column(db.String, primary_key = True)
    password = db.Column(db.String, nullable = False)