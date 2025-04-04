import tkinter as tk
from userLogin import LoginPage

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("TradeWise")
        self.root.geometry("800x650")
        
        self.showLoginPage()

    def showLoginPage(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        LoginPage(self.root, self.showSidebar)

    def showSidebar(self, username):
        from leftNavigation import Sidebar

        for widget in self.root.winfo_children():
            widget.destroy()

        Sidebar(self.root, username, self.showLoginPage)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()