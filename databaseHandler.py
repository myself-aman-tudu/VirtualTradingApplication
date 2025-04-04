import sqlite3
import os
from datetime import datetime

dbPath = os.path.join(os.path.dirname(__file__), "assets", "clientData.db")

def getPortfolioValue(username):
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute("SELECT portfolioValue FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def updatePortfolioValue(username, newValue):
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET portfolioValue = ? WHERE username = ?", (newValue, username))
    conn.commit()
    conn.close()

def addTransaction(username, ticker, transactionType, quantity, pricePerShare, totalValue, portfolioBefore, portfolioAfter):
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    transactionDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO transactions (username, ticker, transaction_type, quantity, price_per_share, total_value, portfolio_value_before, portfolio_value_after, transaction_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, ticker, transactionType, quantity, pricePerShare, totalValue, portfolioBefore, portfolioAfter, transactionDate))
    conn.commit()
    conn.close()
def getTotalInvestment(username):
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT SUM(total_value)
        FROM transactions
        WHERE username = ? AND transaction_type = 'BUY'
    ''', (username,))
    totalInvested = cursor.fetchone()[0] or 0

    cursor.execute('''
        SELECT SUM(total_value)
        FROM transactions
        WHERE username = ? AND transaction_type = 'SELL'
    ''', (username,))
    totalSold = cursor.fetchone()[0] or 0
    conn.close()
    return totalInvested, totalSold
    

def getBoughtStocks(username):
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ticker, 
               SUM(CASE WHEN transaction_type = 'BUY' THEN quantity ELSE -quantity END) AS total_quantity,
               CASE 
                   WHEN SUM(CASE WHEN transaction_type = 'BUY' THEN quantity ELSE -quantity END) > 0
                   THEN SUM(CASE WHEN transaction_type = 'BUY' THEN quantity * price_per_share ELSE 0 END) / 
                        SUM(CASE WHEN transaction_type = 'BUY' THEN quantity ELSE 0 END)
                   ELSE 0
               END AS avg_price_per_share,
               MIN(transaction_date) AS first_purchase_date
        FROM transactions 
        WHERE username = ?
        GROUP BY ticker
        HAVING total_quantity > 0
    """, (username,))
    
    stocks = cursor.fetchall()  # Fetch aggregated results
    conn.close()
    return stocks  

def getTransactionDetails(username):
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT ticker, quantity, total_value, transaction_date, transaction_type
        FROM transactions
        WHERE username = ?
        ORDER BY tid DESC
    ''', (username,))
    
    transactions = cursor.fetchall()  # Returns a list of tuples
    return transactions
