import tkinter as tk
from tkinter import Canvas, Scrollbar, Frame, Label
from todayPrice import findTodayPrice
from userSession import get_loggedInUser
from databaseHandler import getBoughtStocks, getPortfolioValue, updatePortfolioValue, addTransaction, getTotalInvestment, getTransactionDetails

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
def getName(ticker):
    return next((x for x, y in companyToTicker.items() if y == ticker), None)

def getProfitLoss(username):
    totalInvested, totalSold = getTotalInvestment(username)
    hold = [(ticker, quantity) for ticker, quantity, _, _ in getBoughtStocks(username)]
    totalHold = sum(findTodayPrice(ticker)*quantity for ticker, quantity in hold)
    return totalInvested - totalSold, totalHold

def showPortfolioScreen(parent, username):
    canvas = Canvas(parent, bg="#E3F2FD") 
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    scrollFrame = Frame(canvas, bg="#E3F2FD")
    canvas.create_window((0, 0), window=scrollFrame, anchor="n", width=800)  

    canvas.configure(yscrollcommand=scrollbar.set)

    investedValue, currentValue = getProfitLoss(username)
    profit = currentValue - investedValue
    profitPercent = (profit * 100 / investedValue) if investedValue != 0 else 0

    top_frame = Frame(scrollFrame, pady=20, padx=20, bg="#E3F2FD")
    top_frame.pack(fill="x", pady=10)

    Label(top_frame, text=f"Invested: ₹{investedValue:.2f}", font=("Arial", 14), bg="#E3F2FD").grid(row=0, column=0, padx=10)
    Label(top_frame, text=f"Current: ₹{currentValue:.2f}", font=("Arial", 14), bg="#E3F2FD").grid(row=0, column=1, padx=10)
    
    plText = f"{profit:+.2f} ({profitPercent:.2f}%)"
    plColor = "green" if profit >= 0 else "red"
    Label(top_frame, text=f"P&L: {plText}", font=("Arial", 14), fg=plColor, bg="#E3F2FD").grid(row=1, column=0, columnspan=2, pady=10)

    transactionList = getTransactionDetails(username)

    for index, transaction in enumerate(transactionList):
        transactionFrame = Frame(scrollFrame, bg="#BBDEFB", bd=2, relief="ridge", height=100, width=700)
        transactionFrame.pack(fill="x", pady=10, padx=50)

        companyName = getName(transaction[0])  

        top_line = Frame(transactionFrame, bg="#BBDEFB")
        top_line.pack(fill="x", pady=5, padx=10)

        Label(top_line, text=f"{companyName}", font=("Arial", 12, "bold"), bg="#BBDEFB").pack(side="left")

        Label(top_line, text=f"{transaction[4]}", font=("Arial", 12), bg="#BBDEFB", fg="green" if transaction[4] == "Buy" else "red").pack(side="right")

        bottom_line = Frame(transactionFrame, bg="#BBDEFB")
        bottom_line.pack(fill="x", pady=5, padx=10)

        quantity_text = f"Quantity: {transaction[1]:.8f}"  # Display up to 6 decimal places
        Label(bottom_line, text=quantity_text, font=("Arial", 10), bg="#BBDEFB").pack(side="left")

        Label(bottom_line, text=f"Total Value: ₹{transaction[2]:.2f}", font=("Arial", 10), bg="#BBDEFB").pack(side="right")

    scrollFrame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def createPortfolioUI(parent):
    for widget in parent.winfo_children():
        widget.destroy()
    showPortfolioScreen(parent, get_loggedInUser())



