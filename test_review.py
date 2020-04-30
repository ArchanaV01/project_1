import unittest
from Testhelp import Testhelp
from methods import review_exists
from schema import Review


class Test_review(Testhelp):

    def test_valid1(self):
        flag = review_exists('Saimegha','0380795272')
        self.assertTrue(flag)

    def test_invalid1(self):
        flag = review_exists('Saimegha', '1857231082')
        self.assertFalse(flag)

    def test_valid2(self):
        flag = review_exists('Prasanna','0380795272')
        self.assertTrue(flag)

if __name__ == "__main__":
       unittest.main()
