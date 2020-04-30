import unittest
from Testhelp import Testhelp
from application import isStrong

class Test_strongPassword(Testhelp):

    def test_valid1(self):
        flag = isStrong('abcA@123_')
        self.assertTrue(flag)
    
    def test_valid1(self):
        flag = isStrong('ABCabc$$12')
        self.assertTrue(flag)

    def test_invalid1(self):
        flag = isStrong('abcdefcgh')
        self.assertFalse(flag)

    def test_invalid2(self):
        flag = isStrong('abcdAB12')
        self.assertFalse(flag)

if __name__ == "__main__":
       unittest.main() 