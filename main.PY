import talib
import yfinance as yf 
import pandas as pd
import datetime as dt
b=input("enter the  name of the stock : ")
DATA=yf.download(tickers=b)

# DATAMACD=data[MACD]
print(DATA)
