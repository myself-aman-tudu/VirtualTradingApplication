import tkinter as tk
from mainFrame import MainFrame
from orders import OrdersScreen
from userSession import get_loggedInUser, clear_loggedInUser 
class Sidebar:
    def __init__(self, root, username, onSignOut):
        self.root = root
        self.username = username
        self.onSignOut = onSignOut

        self.sidebarFrame = tk.Frame(root, bg="#1A237E", width=200)
        self.sidebarFrame.grid(row=0, column=0, sticky="nsw")

        self.mainFrame = MainFrame(root)

        root.grid_columnconfigure(0, minsize=200)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)
        
        self.createSidebar()

    def createSidebar(self):
        tk.Label(self.sidebarFrame, text=f"Welcome, {self.username}", fg="white", bg="#1A237E", font=("Arial", 14)).pack(pady=10)

        buttons = [
            ("Home", None),
            ("WatchList", self.mainFrame.showStockPrice),
            ("Buy Stocks", self.mainFrame.showOrdersScreen),
            ("Sell Stocks", self.mainFrame.showSellScreen),
            ("Portfolio", self.mainFrame.showPortFolio),
            ("Settings", None),
            ("Sign Out", self.signOut)
        ]

        for btnText, btnCommand in buttons:
            tk.Button(self.sidebarFrame, text=btnText, font=("Arial", 14), bg="#3f51b5", fg="white",
                      command=btnCommand if btnCommand else None, relief="flat", activebackground="#5c6bc0").pack(fill="x", pady=5)

    def signOut(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            clear_loggedInUser()
        self.onSignOut()
