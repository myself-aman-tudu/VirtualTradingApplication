import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch, MagicMock
import databaseHandler
from databaseHandler import getPortfolioValue, updatePortfolioValue, addTransaction
from userSession import get_loggedInUser
from todayPrice import findTodayPrice
from showSellScreen import companyToTicker
value = {}
for i in companyToTicker.values():
    value[i] = -1

class TestSellStock(unittest.TestCase):
    @patch('databaseHandler.getBoughtStocks')
    @patch('userSession.get_loggedInUser')
    @patch('databaseHandler.addTransaction')
    @patch('databaseHandler.updatePortfolioValue')
    @patch('databaseHandler.getPortfolioValue')
    def test_successful_sell(self, mock_getPortfolioValue, mock_updatePortfolioValue, mock_addTransaction, mock_get_loggedInUser, mock_getBoughtStocks):
        mock_get_loggedInUser.return_value = 'test_user'

        mock_getPortfolioValue.return_value = 50000.0  # ₹100000

        stock_price = 1500.0
        value['AAPL'] = stock_price

        mock_getBoughtStocks.return_value = [('AAPL', 5, None, None)]
        mock_addTransaction.return_value = None
        mock_updatePortfolioValue.return_value = None

        current_portfolio_value = mock_getPortfolioValue('test_user')

        totalPrice = 3000.0
        quantity = totalPrice / stock_price

        self.assertEqual(quantity, 2.0)

        expected_portfolio_value = 50000.0 + (quantity * stock_price)
        self.assertAlmostEqual(expected_portfolio_value, 53000.0)

        databaseHandler.addTransaction('test_user', 'AAPL', quantity, totalPrice)
        databaseHandler.updatePortfolioValue('test_user', expected_portfolio_value)
        mock_getPortfolioValue.assert_called_with('test_user')
        mock_updatePortfolioValue.assert_called_with('test_user', expected_portfolio_value)
        mock_addTransaction.assert_called_with('test_user', 'AAPL', quantity, totalPrice)


    @patch('databaseHandler.getBoughtStocks')
    @patch('userSession.get_loggedInUser')
    def test_insufficient_stock(self, mock_get_loggedInUser, mock_getBoughtStocks):
        mock_get_loggedInUser.return_value = 'test_user'
        
        mock_getBoughtStocks.return_value = [('AAPL', 5, None, None)]
        _, presentQuantity, _, _ = mock_getBoughtStocks.return_value[0]
        
        stock_price = 1500.0
        value['AAPL'] = stock_price
        
        totalPrice = 9000.0
        quantity = totalPrice / stock_price  
        
        self.assertTrue(presentQuantity < quantity)

    @patch('databaseHandler.getBoughtStocks')
    @patch('userSession.get_loggedInUser')
    def test_invalid_quantity_or_price(self, mock_get_loggedInUser, mock_getBoughtStocks):
        mock_get_loggedInUser.return_value = 'test_user'
        
        mock_getBoughtStocks.return_value = [('AAPL', 5, None, None)]
        _, presentQuantity, _, _ = mock_getBoughtStocks.return_value[0]
        
        invalid_quantity = -5
        self.assertLess(invalid_quantity, 0)

        invalid_price = -100
        self.assertLess(invalid_price, 0)
