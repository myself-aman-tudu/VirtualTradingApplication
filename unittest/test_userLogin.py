import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from unittest.mock import patch
import tkinter as tk

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from userLogin import LoginPage  

class TestUserLogin(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = LoginPage(self.root, onLoginSuccess=lambda x: None)  

    @patch('tkinter.messagebox.showerror')
    def test_empty_username_or_password(self, mock_showerror):
        self.app.showLoginFields()  
        self.app.entryUsername.insert(0, "")  
        self.app.entryPassword.insert(0, "password")
        self.app.authenticate("login")
        mock_showerror.assert_called_once_with("Error", "Username & password cannot be empty")

    @patch('tkinter.messagebox.showinfo')
    def test_successful_registration(self, mock_showinfo):
        self.app.showRegisterFields()  
        self.app.entryUsername.insert(0, "newuser")
        self.app.entryPassword.insert(0, "password")
        self.app.reEntryPassword.insert(0, "password")
        self.app.authenticate("register")
        mock_showinfo.assert_called_once_with("Success", "User registered successfully")

    @patch('tkinter.messagebox.showinfo')
    def test_successful_login(self, mock_showinfo):
        self.app.showRegisterFields()  
        self.app.entryUsername.insert(0, "newuser")
        self.app.entryPassword.insert(0, "password")
        self.app.authenticate("login")
        mock_showinfo.assert_called_once_with("Success", "Welcome, newuser")

    @patch('tkinter.messagebox.showerror')
    def test_unsuccessful_login(self, mock_showerror):
        self.app.showRegisterFields()  
        self.app.entryUsername.insert(0, "newuser")
        self.app.entryPassword.insert(0, "password1")
        self.app.authenticate("login")
        mock_showerror.assert_called_once_with("Error", "Invalid credentials")
    @patch('tkinter.messagebox.showerror')
    def test_mismatched_passwords(self, mock_showerror):
        self.app.showRegisterFields()  # Ensure entry fields are created
        self.app.entryUsername.insert(0, "newuser")
        self.app.entryPassword.insert(0, "password1")
        self.app.reEntryPassword.insert(0, "password2")
        self.app.authenticate("register")
        mock_showerror.assert_called_once_with("Error", "Passwords do not match")
    @patch('tkinter.messagebox.showerror')
    def test_existing_user_registration(self, mock_showerror):
        self.app.showRegisterFields()  
        
        self.app.entryUsername.insert(0, "existinguser")
        self.app.entryPassword.insert(0, "password123")
        self.app.reEntryPassword.insert(0, "password123")  

        self.app.db.registerUser = lambda username, password: False
        
        self.app.authenticate("register")
        
        mock_showerror.assert_called_once_with("Error", "Username already exists")
    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
