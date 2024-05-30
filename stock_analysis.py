import talib
import pandas as pd
import numpy as np
import datetime
from binance_client import BinanceClient

class Stock:
    def __init__(self, ticker, startdate, enddate, binance_client):
        self.ticker = ticker
        self.startdate = startdate
        self.enddate = enddate
        self.binance_client = binance_client

    def fetch_data(self):
        historical_data = self.binance_client.get_klines(self.ticker, interval='1d', limit=1000)
        print(historical_data)
        data = pd.DataFrame.from_dict(historical_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        print(data)
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
        data["signal1"] = np.where((data["EMA3"] < data["close"]) & (data["close"] < data["EMA1"]) & (data["MACD"] < 0), 1, np.where((data["EMA1"] > data["close"]) & (data["close"] > data["EMA3"]) & (data["MACD"] > 0), -1, 0))
        data["signal2"] = np.where(data["RSI"] > 70, -1, np.where(data["RSI"] < 30, 1, 0))
        data["signal3"] = np.where((data["signal1"] == 1) & (data["signal2"] == 1), 1, 0)
        return data

    def run_analysis(self):
        raw_data = self.fetch_data()
        print(raw_data)
        data_indicator = self.indicator(raw_data)
        data_signal = self.signal(data_indicator)
        return data_signal

    def execute_trades(self, data_signal):
        for index, row in data_signal.iterrows():
            if row['signal2'] == 1:
                print(f"Buy signal detected on {index} for {self.ticker}. Placing order.")
                self.binance_client.place_order(self.ticker, "BUY", "MARKET", 0.01)  
            elif row['signal2'] == -1:
                print(f"Sell signal detected on {index} for {self.ticker}. Placing order.")
                self.binance_client.place_order(self.ticker, "SELL", "MARKET", 0.01)  

if __name__ == "__main__":
    api_key = "88e262c5697a9971f573a9c078d0956ad1bc5fb77a81eeae535952c8f8635637"
    api_secret_key = "b27ce9a1ee11b3cad52b1a7248222feb1394c39c3896fb1c9868ded2bf3a1a6e"

    binance_client = BinanceClient(api_key, api_secret_key)

    if binance_client.login():
        stocks = ['BTCUSDT','BCHUSDT','ETHUSDT','ETCUSDT','LTCUSDT','XRPUSDT','EOSUSDT']
        startdate = datetime.datetime(2015, 1, 4)
        enddate = datetime.datetime(2024, 1, 4)
        for stock_symbol in stocks:
            stock_analysis = Stock(stock_symbol, startdate, enddate, binance_client)
            result = stock_analysis.run_analysis()
            filename = f"{stock_symbol}_data.csv"  # Construct filename
            result.to_csv(filename)  # Write data to CSV
            print(f"Analysis completed for {stock_symbol} and saved to {filename}")
            stock_analysis.execute_trades(result)
    else:
        print("Cannot proceed without valid API credentials.")
