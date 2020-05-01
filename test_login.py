import unittest
from Testhelp import Testhelp
from methods import get_login_details
from schema import User

class Test_getlogin(Testhelp):

    def test_valid(self):
        flag = get_login_details('Prasanna')
        self.assertEqual(flag,1)
    
    def test_not_present(self):
        flag = get_login_details('qwer')
        self.assertEqual(flag,0)
    
if __name__ == "__main__":
       unittest.main()    