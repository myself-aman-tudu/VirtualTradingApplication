import tkinter as tk
from tkinter import ttk
import yfinance as yf

class OrdersScreen:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent, padx=10, pady=10)
        self.frame.pack()
        
        self.companyToTicker = {
            "Apple": "AAPL",
            "Tesla": "TSLA",
            "NVIDIA": "NVDA",
            "Google": "GOOGL",
            "Microsoft": "MSFT",
            "Amazon": "AMZN",
            "Meta (Facebook)": "META",
            "Netflix": "NFLX",
            "Berkshire Hathaway": "BRK-B",
            "JPMorgan Chase": "JPM"
        }
        
        self.createUI()
        
    def createUI(self):
        title = tk.Label(self.frame, text="Stock Prices Today", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        self.tree = ttk.Treeview(self.frame, columns=("Company", "Price"), show="headings")
        self.tree.heading("Company", text="Company Name")
        self.tree.heading("Price", text="Stock Price (USD)")
        self.tree.column("Company", width=200, anchor="w")
        self.tree.column("Price", width=100, anchor="center")
        self.tree.pack()
        
        self.loadStockPrices()
        
    def loadStockPrices(self):
        for company, ticker in self.companyToTicker.items():
            stock = yf.Ticker(ticker)
            price = stock.history(period="1d").iloc[-1].Close  # Fetch latest close price
            self.tree.insert("", "end", values=(company, f"${price:.2f}"))