import sqlite3
import os

class Database:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(__file__), "assets", "clientData.db")
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT ,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                phoneNumber TEXT,
                pan TEXT,
                bankAccount TEXT,
                portfolioValue REAL DEFAULT 100000
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions(
                tid INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                ticker TEXT NOT NULL,
                transaction_type TEXT NOT NULL, -- 'BUY' or 'SELL'
                quantity INTEGER NOT NULL,
                price_per_share REAL NOT NULL,
                total_value REAL NOT NULL,
                portfolio_value_before REAL NOT NULL,
                portfolio_value_after REAL NOT NULL,
                transaction_date TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        ''')
        self.conn.commit()

    def registerUser(self, username, password):
        try:
            self.cursor.execute(
            """INSERT INTO users (username, password, name, email, phoneNumber, pan, bankAccount, portfolioValue) VALUES (?, ?, '', '', '', '', '', 100000)""",
            (username, password)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print("IntegrityError:", e)

    def loginUser(self, username, password):
        """Checks user credentials. Returns True if valid, else False."""
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return bool(self.cursor.fetchone())
