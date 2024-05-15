import talib
import yfinance as yf 
import pandas as pd
import numpy as np
import datetime

class Stock:
    def __init__(self,ticker,startdate,enddate):
        self.ticker=ticker
        self.startdate=startdate
        self.enddate=enddate
        
    def fetch_data(self):
        data = yf.download(self.ticker, start=self.startdate, end=self.enddate)
        data.drop("Adj Close", axis=1, inplace=True)
        return data

    def indicator(self,data):
        data["EMA1"] = talib.EMA(data["High"], timeperiod=200)
        data["EMA2"] = talib.EMA(data["Close"], timeperiod=200)
        data["EMA3"] = talib.EMA(data["Low"], timeperiod=200)
        data["MACD"], _, _ = talib.MACD(data["Close"])
        data["RSI"] = talib.RSI(data["Close"],timeperiod=14)
        return data
    def signal(self,data):
        data["signal1"] = np.where((data["EMA3"] < data["Close"]) & (data["Close"] < data["EMA1"]) & (data["MACD"] < 0), 1,np.where((data["EMA1"] > data["Close"]) & (data["Close"] > data["EMA3"]) & (data["MACD"]>0),-1,0))
        data["signal2"]=np.where(data["RSI"]>70 ,-1,np.where(data["RSI"]<30,1,0))
        data["signal3"]=np.where((data["signal1"]==1) & (data["signal2"]==1),1,0)
        return data
    def run_analysis(self):
        raw_data = self.fetch_data()
        data_indicator = self.indicator(raw_data)
        data_signal = self.signal(data_indicator)
        data_signal.to_csv('stock_data.csv')
        return data_signal
stocks = [
    'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'BRK-A', 'BRK-B', 'JPM', 'JNJ',
    'V', 'WMT', 'PG', 'NVDA', 'MA', 'DIS', 'UNH', 'HD', 'PYPL', 'BAC', 
    'CMCSA', 'INTC', 'ADBE', 'ASML', 'NFLX', 'TSM', 'KO', 'PFE', 'PEP', 'VZ'
]
startdate = datetime.datetime(2015, 1, 4)
enddate = datetime.datetime(2024, 1, 4)

for stock_symbol in stocks:
    stock_analysis = Stock(stock_symbol, startdate, enddate)
    result = stock_analysis.run_analysis()
    print(f"Analysis completed for {stock_symbol}")
