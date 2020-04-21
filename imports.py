import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main(): 
    f = open("books.csv")
    reader = csv.reader(f) 
    next(reader, None)
    try:
        db.execute("CREATE TABLE BOOKS (ISBN VARCHAR PRIMARY KEY, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year VARCHAR NOT NULL)")
    except Exception as e:
        print(e)
    counter = 0
    for isbn, title, author, year in reader:
        counter += 1
        try:
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", 
            {"isbn": isbn, "title": title, "author": author, "year": year}) 
            db.commit()
        except:
            print(isbn, counter)
            continue

if __name__ == "__main__": 
    main()


