import tkinter as tk
from showStockPrice import createStockUI
from showOrdersScreen import createOrdersUI
from showSellScreen import createSellUI
from viewPortfolio import createPortfolioUI

class MainFrame:
    def __init__(self, root):
        self.root = root
        self.mainFrame = tk.Frame(root, bg="white")
        self.mainFrame.grid(row=0, column=1, sticky="nsew")


    def clearFrame(self):
        for widget in self.mainFrame.winfo_children():
            widget.destroy()

    def showStockPrice(self):
        self.clearFrame()
        createStockUI(self.mainFrame)

    def showOrdersScreen(self):
        self.clearFrame()
        createOrdersUI(self.mainFrame)

    def showSellScreen(self):
        self.clearFrame()
        createSellUI(self.mainFrame)

    def showPortFolio(self):
        self.clearFrame()
        createPortfolioUI(self.mainFrame)
