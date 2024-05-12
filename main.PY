import talib
import yfinance as yf 
import pandas as pd
import numpy as np
import datetime

startdate = datetime.datetime(2015, 1, 4)
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
    data["MACD"], _, _ = talib.MACD(data["Close"])
    data["RSI"] = talib.RSI(data["Close"],timeperiod=14)
    return data
#1LONG 
#0NOTHING
#-1SHORT
#one more indicator

def signal(data):
    data["signal1"] = np.where((data["EMA3"] < data["Close"]) & (data["Close"] < data["EMA1"]) & (data["MACD"] < 0), 1,np.where((data["EMA1"] > data["Close"]) & (data["Close"] > data["EMA3"]) & (data["MACD"]>0),-1,0))
    data["signal2"]=np.where(data["RSI"]>70 ,-1,np.where(data["RSI"]<30,1,0))
    data["signal3"]=np.where((data["signal1"]==1) & (data["signal2"]==1),1,0)
    return data
raw_data = fetchdata(ticker)
data_indicator = indicator(raw_data)
data_signal= signal(data_indicator)
data_signal.to_csv('stock_data.csv')
print(data_signal)
