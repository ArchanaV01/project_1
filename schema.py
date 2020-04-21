from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "USERS"
    name = db.Column(db.String, primary_key = True)
    password = db.Column(db.String, nullable = False)
    created_at = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)