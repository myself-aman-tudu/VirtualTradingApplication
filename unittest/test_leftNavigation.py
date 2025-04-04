import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
import re
from unittest.mock import MagicMock, patch
import tkinter as tk
from leftNavigation import Sidebar

class TestSidebar(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.username = "testuser"
        self.onSignOut = MagicMock()
        self.sidebar = Sidebar(self.root, self.username, self.onSignOut)
        self.root.update()  

    @patch('tkinter.messagebox.showinfo')
    def test_sidebar_creation(self, mock_showinfo):
        sidebar_label = self.sidebar.sidebarFrame.winfo_children()[0]
        self.assertEqual(sidebar_label.cget("text"), f"Welcome, {self.username}")

    def test_sign_out_button(self):
        self.sidebar.signOut()
        self.onSignOut.assert_called_once()



    def test_button_commands(self):
        button_commands = {btn.cget('text'): btn.cget('command') for btn in self.sidebar.sidebarFrame.winfo_children() if isinstance(btn, tk.Button)}

        for text, cmd in button_commands.items():
            print(f"Button '{text}' command: {cmd}")
        
        def extract_command_name(cmd):
            if isinstance(cmd, str) and cmd: 
                match = re.search(r'[A-Za-z_]\w*$', cmd)
                return match.group(0) if match else None
            elif callable(cmd):  
                return cmd.__name__
            return None

        if button_commands.get('Home'):
            home_command_name = extract_command_name(button_commands.get('Home'))
            expected_home_name = self.sidebar.mainFrame.showStockPrice.__name__
            self.assertEqual(home_command_name, expected_home_name, "Home button should call 'showStockPrice'")
        
        if button_commands.get('Buy Stocks'):
            buy_stocks_command_name = extract_command_name(button_commands.get('Buy Stocks'))
            expected_buy_stocks_name = self.sidebar.mainFrame.showOrdersScreen.__name__
            self.assertEqual(buy_stocks_command_name, expected_buy_stocks_name, "Buy Stocks button should call 'showOrdersScreen'")

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
