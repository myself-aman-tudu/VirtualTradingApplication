import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from clientDataCreate import Database
from userSession import set_loggedInUser, clear_loggedInUser

class LoginPage:
    def __init__(self, root, onLoginSuccess):
        self.root = root
        self.onLoginSuccess = onLoginSuccess
        self.db = Database()

        self.root.geometry("800x650")
        self.root.title("TradeWise")

        self.backgroundFrame = tk.Frame(self.root)
        self.backgroundFrame.place(relwidth=1, relheight=1)

        self.backgroundImage = Image.open("assets/plainbluebackground.jpg")
        self.backgroundImage = self.backgroundImage.resize((800, 650), Image.LANCZOS)
        self.bgImageTk = ImageTk.PhotoImage(self.backgroundImage)

        self.bgLabel = tk.Label(self.backgroundFrame, image=self.bgImageTk)
        self.bgLabel.place(relwidth=1, relheight=1)

        self.foregroundFrame = tk.Frame(self.root, bg="white", bd=2)
        self.foregroundFrame.place(relx=0.4, rely=0.1, relwidth=0.55, relheight=0.8)

        self.createInitialScreen()

    def createInitialScreen(self):
        for widget in self.foregroundFrame.winfo_children():
            widget.destroy()

        welcomeLabel = tk.Label(self.foregroundFrame, text="Welcome Back", font=("Helvetica", 35), bg="white", anchor="w")
        welcomeLabel.pack(pady=30, padx=20, anchor="w")

        signInLabel = tk.Label(self.foregroundFrame, text="Sign in to your account", font=("Helvetica", 14), bg="white", anchor="w")  
        signInLabel.pack(pady=(10, 5), padx=20, anchor="w")

        signInButton = tk.Button(self.foregroundFrame, text="Sign In", font=("Helvetica", 15, "bold"), command=self.showLoginFields, bg="white", fg="#1A237E",  activebackground="#cce5ff", relief="flat", width=6, height=1)
        signInButton.pack(pady=10, padx=20, anchor="w")

        signUpLabel = tk.Label(self.foregroundFrame, text="Don't have an account?", font=("Helvetica", 14), bg="white", anchor="w")  
        signUpLabel.pack(pady=(30, 5), padx=20, anchor="w")

        signUpButton = tk.Button(self.foregroundFrame, text="Sign Up", font=("Helvetica", 15, "bold"),  command=self.showRegisterFields, bg="#3399FF", fg="white",  activebackground="#66b3ff", relief="flat", width=6, height=1)
        signUpButton.pack(pady=10, padx=20, anchor="w")

    def showLoginFields(self):
        self.showAuthFields(action="login")

    def showRegisterFields(self):
        self.showAuthFields(action="register")

    def showAuthFields(self, action):
        for widget in self.foregroundFrame.winfo_children():
            widget.destroy()

        tk.Label(self.foregroundFrame, text="Username:", font=("Helvetica", 14), bg="white").pack(pady=10)
        self.entryUsername = tk.Entry(self.foregroundFrame, font=("Helvetica", 12))
        self.entryUsername.pack()

        tk.Label(self.foregroundFrame, text="Password:", font=("Helvetica", 14), bg="white").pack(pady=10)
        self.entryPassword = tk.Entry(self.foregroundFrame, show="*", font=("Helvetica", 12))
        self.entryPassword.pack()

        if action == "register":
            tk.Label(self.foregroundFrame, text="Re-Enter Password:", font=("Helvetica", 14), bg="white").pack(pady=10)
            self.reEntryPassword = tk.Entry(self.foregroundFrame, show="*", font=("Helvetica", 12))
            self.reEntryPassword.pack()

        actionButton = tk.Button(self.foregroundFrame, text="Proceed", command=lambda: self.authenticate(action), font=("Helvetica", 14), bg="#3399FF", fg="white", activebackground="#66b3ff", relief="flat")
        actionButton.pack(pady=20)

        backButton = tk.Button(self.foregroundFrame, text="Back", command=self.createInitialScreen, font=("Helvetica", 14), bg="white", fg="#3399FF", activebackground="#cce5ff", relief="flat")
        backButton.pack(pady=10)

    def authenticate(self, action):
        username = self.entryUsername.get().strip()
        password = self.entryPassword.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username & password cannot be empty")
            return

        if action == "login":
            if self.db.loginUser(username, password):
                set_loggedInUser(username)
                messagebox.showinfo("Success", f"Welcome, {username}")
                self.onLoginSuccess(username)
            else:
                messagebox.showerror("Error", "Invalid credentials")
        elif action == "register":
            password2 = self.reEntryPassword.get().strip()
            if password != password2:
                messagebox.showerror("Error", "Passwords do not match")
                return
            if self.db.registerUser(username, password):
                messagebox.showinfo("Success", "User registered successfully")
                self.createInitialScreen()
            else:
                messagebox.showerror("Error", "Username already exists")
