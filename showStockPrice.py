import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

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

def createStockUI(parent):
    global stockVar, stockDropdown, loadStockButton, backButton, resetButton, imageLabel, statusLabel, yearVar, stockFrame, yearDropdown, loadYearButton

    parent.configure(bg="white")
    
    def showYearOptions():
        global yearDropdown, loadYearButton, yearVar
        selectedStock = stockVar.get()

        if selectedStock == "Select a stock":
            statusLabel.config(text="Please select a stock first!", fg="red")
            statusLabel.pack()
            return

        statusLabel.config(text="")
        statusLabel.pack_forget()
        stockDropdown.pack_forget()
        loadStockButton.pack_forget()

        yearVar = tk.StringVar()
        yearVar.set("Select a time period")
        
        yearDropdown = ttk.Combobox(stockFrame, textvariable=yearVar, values=["5 Years", "10 Years"], state="readonly", font=("Arial", 12))
        yearDropdown.pack(pady=5)

        loadYearButton = tk.Button(stockFrame, text="Show Stock Chart", command=showImage, bg="#4CAF50", fg="white", font=("Arial", 12), relief="raised")
        loadYearButton.pack(pady=5)

        backButton.config(command=resetToStockSelection)
        backButton.pack(pady=5)

    def showImage():
        selectedStock = stockVar.get()

        if selectedStock not in companyToTicker:
            statusLabel.config(text="Invalid stock selected", fg="red")
            statusLabel.pack()
            return

        selectedYear = yearVar.get()
        if selectedYear == "Select a time period":
            statusLabel.config(text="Please select a time period!", fg="red")
            statusLabel.pack()
            return

        ticker = companyToTicker[selectedStock]
        yearNumber = "5" if "5 Years" in selectedYear else "10"
        imagePath = f"assets/{ticker}{yearNumber}.png"

        yearDropdown.pack_forget()
        loadYearButton.pack_forget()
        backButton.pack_forget()

        if os.path.exists(imagePath):
            img = Image.open(imagePath)
            img = img.resize((1200, 700), Image.LANCZOS)
            image = ImageTk.PhotoImage(img)
            
            imageLabel.pack(pady=10)
            imageLabel.config(image=image)
            imageLabel.image = image

            statusLabel.config(text=f"Showing: {selectedStock} ({selectedYear})", fg="green")
        else:
            statusLabel.config(text=f"No image found for {selectedStock} ({selectedYear})", fg="red")

        statusLabel.pack()
        resetButton.pack(pady=5)

        backButton.config(command=resetToYearSelection)
        backButton.pack(pady=5)

    def resetToStockSelection():
        stockDropdown.pack(pady=10)
        loadStockButton.pack(pady=10)
        yearDropdown.pack_forget()
        loadYearButton.pack_forget()
        imageLabel.pack_forget()
        statusLabel.pack_forget()
        backButton.pack_forget()
        resetButton.pack_forget()

    def resetToYearSelection():
        imageLabel.pack_forget()
        statusLabel.pack_forget()

        yearVar.set("Select a time period")
        yearDropdown.pack(pady=5)
        loadYearButton.pack(pady=5)

        backButton.config(command=resetToStockSelection)
        backButton.pack(pady=5)

        resetButton.pack_forget()

    def resetApp():
        resetButton.pack_forget()
        stockVar.set("Select a stock")
        resetToStockSelection()

    stockFrame = tk.Frame(parent, bg="white", padx=20, pady=20)
    stockFrame.pack(fill="both", expand=True, padx=10, pady=10)

    titleLabel = tk.Label(stockFrame, text="Stock Price Viewer", font=("Helvetica", 24, "bold"), bg="white", fg="#1A237E")
    titleLabel.pack(pady=20)

    stockVar = tk.StringVar()
    stockVar.set("Select a stock")

    stockDropdown = ttk.Combobox(stockFrame, textvariable=stockVar, values=list(companyToTicker.keys()), state="readonly", font=("Arial", 12))
    stockDropdown.pack(pady=10)

    loadStockButton = tk.Button(stockFrame, text="Select Time Period", command=showYearOptions, bg="#4CAF50", fg="white", font=("Arial", 12), relief="raised")
    loadStockButton.pack(pady=10)

    backButton = tk.Button(stockFrame, text="Back", font=("Arial", 12), bg="#F44336", fg="white", relief="raised")
    backButton.pack_forget()

    imageLabel = tk.Label(stockFrame, bg="white")
    imageLabel.pack_forget()

    statusLabel = tk.Label(stockFrame, text="", font=("Arial", 12), bg="white")
    statusLabel.pack_forget()

    resetButton = tk.Button(stockFrame, text="Reset", command=resetApp, bg="#2196F3", fg="white", font=("Arial", 12), relief="raised")
    resetButton.pack_forget()
