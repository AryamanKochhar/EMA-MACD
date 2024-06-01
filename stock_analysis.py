import talib
import pandas as pd
import numpy as np
import datetime
from binance_client import BinanceClient
import time
import
class Stock:
    def __init__(self, ticker, binance_client):
        self.ticker = ticker
        self.binance_client = binance_client

    def fetch_data(self):
        historical_data = self.binance_client.get_klines(self.ticker, interval='1m', limit=300)
        data = pd.DataFrame(historical_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        data["open"] = data["open"].apply(float)
        data["high"] = data["high"].apply(float)
        data["close"] = data["close"].apply(float)
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
        data.set_index('timestamp', inplace=True)
        return data

    def indicator(self, data):
        data["EMA1"] = talib.EMA(data["high"], timeperiod=200)
        data["EMA2"] = talib.EMA(data["close"], timeperiod=200)
        data["EMA3"] = talib.EMA(data["low"], timeperiod=200)
        data["MACD"], _, _ = talib.MACD(data["close"])
        data["RSI"] = talib.RSI(data["close"], timeperiod=14)
        return data

    def signal(self, data):
    # Signal 1 based on EMA and MACD conditions
        data["signal1"] = np.where((data["EMA3"] < data["close"]) & (data["close"] < data["EMA1"]) & (data["MACD"] < 0), 1, 
                               np.where((data["EMA1"] > data["close"]) & (data["close"] > data["EMA3"]) & (data["MACD"] > 0), -1, 0))
    
    # Signal 2 based on RSI conditions
        data["signal2"] = np.where(data["RSI"].between(60, 70), -1, np.where(data["RSI"].between(0, 40), 1, 0))
    
    # Signal 3 based on signal1 and signal2 conditions
        data["signal3"] = np.where((data["signal1"] == 1) & (data["signal2"] == 1), 1, 
                               np.where((data["signal1"] == -1) & (data["signal2"] == -1), -1, 0))
    
        return data


    def execute_trades(self, data_signal):
        latest_signal = data_signal.iloc[-1]
        print(latest_signal)
        if latest_signal['signal1'] == 1:
            print(f"Buy signal detected for {self.ticker}. Placing order.")
            self.binance_client.place_order(self.ticker, "BUY", "MARKET", 0.01)  
        elif latest_signal['signal1'] == -1:
            print(f"Sell signal detected for {self.ticker}. Placing order.")
            self.binance_client.place_order(self.ticker, "SELL", "MARKET", 0.01)  

    def run_live_analysis(self):
        while True:
            raw_data = self.fetch_data()
            data_indicator = self.indicator(raw_data)
            data_signal = self.signal(data_indicator)
            self.execute_trades(data_signal)
            time.sleep(60)  # Wait for 1 minute before fetching new data

if __name__ == "__main__":
    api_key = "88e262c5697a9971f573a9c078d0956ad1bc5fb77a81eeae535952c8f8635637"
    api_secret_key = "b27ce9a1ee11b3cad52b1a7248222feb1394c39c3896fb1c9868ded2bf3a1a6e"

    binance_client = BinanceClient(api_key, api_secret_key)

    if binance_client.login():
        stocks = ['BTCUSDT','ETHUSDT','ETCUSDT','LTCUSDT','XRPUSDT','EOSUSDT']  # Add more symbols if needed
        for stock_symbol in stocks:
            stock_analysis = Stock(stock_symbol, binance_client)
            stock_analysis.run_live_analysis()
            
    else:
        print("Cannot proceed without valid API credentials.")
