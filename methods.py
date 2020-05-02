from schema import *
from sqlalchemy import and_

def getbook(isbn):
    book = Book.query.get(isbn)
    return book

def review_exists(name, isbn):
    if (Review.query.filter(and_(Review.name==name, Review.isbn==isbn)).all()):
        return True
    else:
        return False

def get_login_details(name):
    obj = User.query.get(name)
    
    if obj is None:
        return 0
    elif (obj.name == name):
        return 1
