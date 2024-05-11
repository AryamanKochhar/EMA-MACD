import talib
import yfinance as yf 
import pandas as pd
import numpy as np
import datetime

startdate = datetime.datetime(2020, 1, 4)
enddate = datetime.datetime(2024, 1, 4)
ticker = input("Enter a stock symbol: ")

def fetchdata(ticker):
    data = yf.download(ticker, start=startdate, end=enddate)
    data.drop("Adj Close", axis=1, inplace=True)
    return data

def indicator(data):
    data["EMA1"] = talib.EMA(data["High"], timeperiod=200)
    data["EMA2"] = talib.EMA(data["Close"], timeperiod=200)
    data["EMA3"] = talib.EMA(data["Low"], timeperiod=200)
# data["MACD"] = talib.MACD(data["Close"])  
    data["MACD"], _, _ = talib.MACD(data["Close"])
    return data

def signal(data):
    data["signal_buy"] = np.where((data["EMA1"] < data["Close"]) & (data["Close"] < data["EMA3"]) & (data["MACD"] < 0), 1, 0)
    return data

a = fetchdata(ticker)
b = indicator(a)
b = signal(b)
b.to_csv('stock_data.csv')
b.to_excel('stock_data.xlsx')
print(b)
