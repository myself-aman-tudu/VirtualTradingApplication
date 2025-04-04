import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import sqlite3
import os
from todayPrice import findTodayPrice
from userSession import get_loggedInUser
from databaseHandler import getBoughtStocks, getPortfolioValue, updatePortfolioValue, addTransaction
from showOrdersScreen import currentPortfolio

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

value = {ticker: findTodayPrice(ticker) for ticker in companyToTicker.values()}

def getName(ticker):
    return next((x for x, y in companyToTicker.items() if y == ticker), None)

def percentChange(pastPrice, presentPrice):
    change = (presentPrice - pastPrice)
    change = change * 100 / pastPrice
    return change

def refreshPriceList():
    global priceList
    priceList = [(getName(ticker), quantity, pastPrice, value[ticker], percentChange(pastPrice, value[ticker])) for ticker, quantity, pastPrice, _ in getBoughtStocks(get_loggedInUser())]

refreshPriceList()

def showAvailableStocks(parent):
    parent.configure(bg="#D6EAF8")
    priceFrame = tk.Frame(parent, bg="#D6EAF8")
    priceFrame.pack(pady=10)
    header_bg = "#2265a1"

    headers = ["Company", "Quantity", "PurchasePrice", "PresentPrice", "Change"]
    for col, header in enumerate(headers):
        tk.Label(priceFrame, text=header, font=("Arial", 14, "bold"), width=18, anchor="center", 
                 bg=header_bg, fg="white").grid(row=0, column=col)

    for i, (company, quantity, pastPrice, presentPrice, change) in enumerate(priceList, start=1):
        tk.Label(priceFrame, text=company, font=("Arial", 12), width=17, anchor="w", bg="#D6EAF8").grid(row=i, column=0)
        tk.Label(priceFrame, text=f"{quantity:.4f}", font=("Arial", 12), width=10, anchor="w", bg="#D6EAF8").grid(row=i, column=1)
        tk.Label(priceFrame, text=f"{pastPrice:.2f}", font=("Arial", 12), width=10, anchor="w", bg="#D6EAF8").grid(row=i, column=2)
        tk.Label(priceFrame, text=f"{presentPrice:.2f}", font=("Arial", 12), width=10, anchor="w", bg="#D6EAF8").grid(row=i, column=3)
        
        change_text = f"{change:+.4f}" if change >= 0 else f"{change:.4f}"
        change_color = "green" if change > 0 else ("red" if change < 0 else "black")

        tk.Label(priceFrame, text=change_text, font=("Arial", 12), width=10, anchor="w", bg="#D6EAF8", 
                fg=change_color).grid(row=i, column=4)

    portfolioFrame = tk.Frame(parent, bg="#D6EAF8")
    portfolioFrame.pack(pady=10)
    availableBalance = currentPortfolio()
    balanceLabel = tk.Label(portfolioFrame, text=f"Available Balance: ₹{availableBalance}", 
                            font=("Arial", 16, "bold"), fg="#154360", bg="#D6EAF8")
    balanceLabel.pack(pady=10)

def showSellOption(parent, username):
    sellFrame = tk.Frame(parent, padx=10, pady=10, relief=tk.RIDGE, borderwidth=2, bg="#D6EAF8")
    sellFrame.pack(pady=10)

    tk.Label(sellFrame, text="SELL STOCK", font=("Arial", 18, "bold"), bg="#D6EAF8").grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(sellFrame, text="Select Stock:", font=("Arial", 12), bg="#D6EAF8").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    stockVar = tk.StringVar()
    stockVar.set("Select a stock")
    stockDropdown = ttk.Combobox(sellFrame, textvariable=stockVar, values=[row[0] for row in priceList], state="readonly")
    stockDropdown.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(sellFrame, text="Enter Quantity:", font=("Arial", 12), bg="#D6EAF8").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    quantityEntry = tk.Entry(sellFrame, font=("Arial", 12))
    quantityEntry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(sellFrame, text="Enter Amount:", font=("Arial", 12), bg="#D6EAF8").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    priceEntry = tk.Entry(sellFrame, font=("Arial", 12))
    priceEntry.grid(row=3, column=1, padx=5, pady=5)

    def sellStock():
        company = stockVar.get()
        ticker = companyToTicker.get(company)
        quantityStr = quantityEntry.get().strip()
        priceStr = priceEntry.get().strip()

        if not company or company == "Select a stock":
            messagebox.showerror("Error", "Please select a stock.")
            return

        try:
            quantity = float(quantityStr) if quantityStr else None
            totalPrice = float(priceStr) if priceStr else None
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price entered.")
            return

        if totalPrice:
            pricePerShare = value[ticker]
            quantity = totalPrice / pricePerShare

        if not quantity or quantity <= 0:
            messagebox.showerror("Error", "Invalid quantity or price entered.")
            return

        stockEntry = next((entry for entry in priceList if entry[0] == company), None)
        
        if not stockEntry:
            messagebox.showerror("Error", "Stock not found in your holdings.")
            return

        availableQuantity = stockEntry[1]
        if quantity > availableQuantity:
            messagebox.showerror("Error", f"Insufficient stock. You own {availableQuantity}, but you tried to sell {quantity}.")
            return

        portfolioBefore = getPortfolioValue(username)
        totalValue = quantity * value[ticker]
        portfolioAfter = portfolioBefore + totalValue
        
        updatePortfolioValue(username, portfolioAfter)
        addTransaction(username, ticker, "SELL", quantity, value[ticker], totalValue, portfolioBefore, portfolioAfter)

        refreshPriceList()
        createSellUI(parent)
        messagebox.showinfo("Success", f"Successfully sold {quantity:.2f} shares of {company}.")


    tk.Button(sellFrame, text="Sell", font=("Arial", 14), command=sellStock, bg="green", fg="white").grid(row=4, column=0, columnspan=2, pady=10)


def createSellUI(parent):
    for widget in parent.winfo_children():
        widget.destroy()
    parent.configure(bg="#D6EAF8")
    refreshPriceList()
    showAvailableStocks(parent)
    showSellOption(parent, get_loggedInUser())

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Stock Selling App")
    createSellUI(root)
    root.mainloop()
