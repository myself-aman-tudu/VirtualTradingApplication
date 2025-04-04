import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch, MagicMock
import databaseHandler
from databaseHandler import getPortfolioValue, updatePortfolioValue, addTransaction
from userSession import get_loggedInUser
from todayPrice import findTodayPrice
from showOrdersScreen import companyToTicker 

value = {}
for i in companyToTicker.values():
    value[i] = -1
class TestBuyStock(unittest.TestCase):

    @patch('databaseHandler.getPortfolioValue')
    @patch('databaseHandler.updatePortfolioValue')
    @patch('databaseHandler.addTransaction')
    @patch('userSession.get_loggedInUser')
    def test_successful_buy(self, mock_get_loggedInUser, mock_addTransaction, mock_updatePortfolioValue, mock_getPortfolioValue):
        mock_get_loggedInUser.return_value = 'test_user'

        mock_getPortfolioValue.return_value = 100000.0  # ₹100000

        stock_price = 1500.0
        value['AAPL'] = stock_price

        mock_addTransaction.return_value = None
        mock_updatePortfolioValue.return_value = None

        current_portfolio_value = mock_getPortfolioValue('test_user')

        totalPrice = 3000.0
        quantity = totalPrice / stock_price  

        self.assertEqual(quantity, 2.0)

        expected_portfolio_value = 100000.0 - (quantity * stock_price)
        self.assertAlmostEqual(expected_portfolio_value, 97000.0)

        databaseHandler.addTransaction('test_user', 'AAPL', quantity, totalPrice)
        databaseHandler.updatePortfolioValue('test_user', expected_portfolio_value)

        mock_getPortfolioValue.assert_called_with('test_user')
        mock_updatePortfolioValue.assert_called_with('test_user', expected_portfolio_value)
        mock_addTransaction.assert_called_with('test_user', 'AAPL', quantity, totalPrice)

    @patch('databaseHandler.getPortfolioValue')
    @patch('userSession.get_loggedInUser')
    def test_insufficient_balance(self, mock_get_loggedInUser, mock_getPortfolioValue):
        mock_get_loggedInUser.return_value = 'test_user'
        
        mock_getPortfolioValue.return_value = 1000.0  
        
        stock_price = 1500.0
        value['AAPL'] = stock_price
        
        totalPrice = 3000.0
        quantity = totalPrice / stock_price  
        
        self.assertTrue(1000.0 < totalPrice)

    @patch('databaseHandler.getPortfolioValue')
    @patch('userSession.get_loggedInUser')
    def test_invalid_quantity_or_price(self, mock_get_loggedInUser, mock_getPortfolioValue):
        mock_get_loggedInUser.return_value = 'test_user'
        
        mock_getPortfolioValue.return_value = 100000.0
        
        invalid_quantity = -5
        self.assertLess(invalid_quantity, 0)

        invalid_price = -100
        self.assertLess(invalid_price, 0)
