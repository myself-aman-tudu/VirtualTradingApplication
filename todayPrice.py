import yfinance as yf

tickers = ["AAPL", "TSLA", "NVDA", "GOOGL", "MSFT", "AMZN", "META", "NFLX", "BRK-B", "JPM"]

def getUSDtoINR():
    forexData = yf.Ticker("USDINR=X")
    exchangeRate = forexData.history(period="1d")["Close"].iloc[0]
    return exchangeRate

def findTodayPrice(ticker):
    try:
        data = yf.Ticker(ticker)
        todayPrice = data.history(period="1d")
        closingPrice = todayPrice["Close"].iloc[0]
        exchange_rate = getUSDtoINR()
        priceInr = closingPrice * exchange_rate
        return priceInr
    except Exception as e:
        return -1