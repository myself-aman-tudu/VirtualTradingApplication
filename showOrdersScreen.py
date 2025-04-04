import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
from todayPrice import findTodayPrice
import sqlite3
from userSession import get_loggedInUser
import os
from databaseHandler import getPortfolioValue, updatePortfolioValue, addTransaction

companyToTicker = {
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
value = {}
for i in companyToTicker.values():
    value[i] = findTodayPrice(i)
priceList = [(company, ticker, value[ticker]) for company, ticker in companyToTicker.items()]



def currentPortfolio():
    username = get_loggedInUser()
    db_path = os.path.join(os.path.dirname(__file__), "assets", "clientData.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT portfolioValue FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return round(result[0], 2) if result else 0


def showTodayPrice(parent):
    parent.configure(bg="#D6EAF8") 
    priceFrame = tk.Frame(parent, bg="#D6EAF8")
    priceFrame.pack(pady=10)

    header_bg = "#2265a1"

    tk.Label(priceFrame, text="Company", font=("Arial", 14, "bold"), width=20, anchor="center", bg=header_bg, fg="white").grid(row=0, column=0)
    tk.Label(priceFrame, text="Ticker", font=("Arial", 14, "bold"), width=15, anchor="center", bg=header_bg, fg="white").grid(row=0, column=1)
    tk.Label(priceFrame, text="Value", font=("Arial", 14, "bold"), width=15, anchor="center", bg=header_bg, fg="white").grid(row=0, column=2)

    # Data rows
    for i, (company, ticker, val) in enumerate(priceList, start=1):
        tk.Label(priceFrame, text=company, font=("Arial", 12), width=20, anchor="w", bg="#D6EAF8").grid(row=i, column=0, padx=10, pady=5)
        tk.Label(priceFrame, text=ticker, font=("Arial", 12), width=15, anchor="center", bg="#D6EAF8").grid(row=i, column=1, padx=10, pady=5)
        tk.Label(priceFrame, text=f"{val:.2f}", font=("Arial", 12), width=15, anchor="center", bg="#D6EAF8").grid(row=i, column=2, padx=10, pady=5)

    # Display available balance
    portfolioFrame = tk.Frame(parent, bg="#D6EAF8")
    portfolioFrame.pack(pady=10)
    availableBalance = currentPortfolio()
    balanceLabel = tk.Label(portfolioFrame, text=f"Available Balance: ₹{availableBalance}", font=("Arial", 16, "bold"), fg="#154360", bg="#D6EAF8")
    balanceLabel.pack(pady=10)


def showBuyOption(parent, username):
    buyFrame = tk.Frame(parent, padx=10, pady=10, relief=tk.RIDGE, borderwidth=2, bg="#D6EAF8")
    buyFrame.pack(pady=10)

    tk.Label(buyFrame, text="BUY STOCK", font=("Arial", 14, "bold"), bg="#D6EAF8", fg="#1A5276").grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(buyFrame, text="Select Stock:", font=("Arial", 12), bg="#D6EAF8").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    stockVar = tk.StringVar()
    stockVar.set("Select a stock")
    stockDropdown = ttk.Combobox(buyFrame, textvariable=stockVar, values=list(companyToTicker.keys()), state="readonly")
    stockDropdown.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(buyFrame, text="Enter Quantity (Shares):", font=("Arial", 12), bg="#D6EAF8").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    quantityEntry = tk.Entry(buyFrame, font=("Arial", 12))
    quantityEntry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(buyFrame, text="Enter Price (INR):", font=("Arial", 12), bg="#D6EAF8").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    priceEntry = tk.Entry(buyFrame, font=("Arial", 12))
    priceEntry.grid(row=3, column=1, padx=5, pady=5)

    def buyStock():
        company = stockVar.get()
        if company == "Select a stock":
            messagebox.showerror("Error", "Please select a stock.")
            return
        ticker = companyToTicker[company]
        quantityStr = quantityEntry.get().strip()
        priceStr = priceEntry.get().strip()

        

        if not quantityStr and not priceStr:
            messagebox.showerror("Error", "Enter either quantity or price to buy.")
            return

        quantity = float(quantityStr) if quantityStr.replace('.', '', 1).isdigit() else None
        totalPrice = float(priceStr) if priceStr.replace('.', '', 1).isdigit() else None

        if totalPrice:
            pricePerShare = value[ticker]  
            if not pricePerShare:
                messagebox.showerror("Error", "Unable to fetch stock price.")
                return
            quantity = totalPrice / pricePerShare  

        if not quantity or quantity <= 0:
            messagebox.showerror("Error", "Invalid quantity or price entered.")
            return

        pricePerShare = value[ticker] 
        totalValue = quantity * pricePerShare

        portfolioBefore = getPortfolioValue(username)
        if portfolioBefore is None:
            messagebox.showerror("Error", "User not found.")
            return

        if portfolioBefore < totalValue:
            messagebox.showerror("Error", "Insufficient balance!")
            return

        portfolioAfter = portfolioBefore - totalValue
        updatePortfolioValue(username, portfolioAfter)
        addTransaction(username, ticker, "BUY", quantity, pricePerShare, totalValue, portfolioBefore, portfolioAfter)

        messagebox.showinfo("Success", f"Successfully bought {quantity:.2f} shares of {ticker} at {pricePerShare} each.")
        quantityEntry.delete(0, tk.END)
        priceEntry.delete(0, tk.END)
        createOrdersUI(parent)

    tk.Button(buyFrame, text="Buy", font=("Arial", 14), command=buyStock).grid(row=4, column=0, columnspan=2, pady=10)
def createOrdersUI(parent):
    for widget in parent.winfo_children():
        widget.destroy()
    showTodayPrice(parent)
    showBuyOption(parent, get_loggedInUser())
