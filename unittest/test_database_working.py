import unittest
import sys
import os
from unittest.mock import patch
import tkinter as tk

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clientDataCreate import Database  

class TestUserLogin(unittest.TestCase):

    def setUp(self):
        self.database = Database()
        
    def test_register_user(self):
        result = self.database.registerUser('testuser', 'password')  
        self.assertTrue(result)

    def test_login_user_success(self):
        self.database.registerUser('testuser2', 'password2')
        result = self.database.loginUser('testuser2', 'password2')  
        self.assertTrue(result)

    def test_login_user_failure(self):
        result = self.database.loginUser('nonexistentuser', 'wrongpassword')  
        self.assertFalse(result)
    def test_login_user_wrong_password(self):
        self.database.registerUser('testuser3', "password3")
        result = self.database.loginUser('testuser3', 'password33')
        self.assertFalse(result)
if __name__ == '__main__':
    unittest.main()