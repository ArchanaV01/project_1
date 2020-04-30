import unittest
from Testhelp import Testhelp
from schema import *
from application import get_books

class Test_Search(Testhelp):

    def test_valid(self):
        books = get_books('I, Robo', 'Title')
        for book in books:
            self.assertEqual(book.title,'I, Robot')
    
    def test_valid1(self):
        books = get_books('V.C. Andrews', '')
        self.assertEqual(len(books),9)

    def test_valid2(self):
        books = get_books('The Sleeping Doll', 'None')
        for book in books:
            self.assertEqual(book.year,'2007')

    def test_valid3(self):
        books = get_books('009', 'Year')
        self.assertEqual(len(books),241)
    
    def test_valid4(self):
        books = get_books('Isaac Asimov', 'Author')
        self.assertEqual(len(books),17)

    def test_invalid(self):
        book = get_books('abcd', 'None')
        self.assertEqual(len(book),0)

if __name__ == "__main__":
       unittest.main() 