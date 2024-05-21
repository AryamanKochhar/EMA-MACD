#broker wrapper
#login function
#getting historical data
# get available balance
# get symbol info 

import json
import time
from binance.client import Client
from binance.streams import BinanceSocketManager

class Broker:
    def __init__(self, api_key=None, api_secret=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = None
        self.bm = None
        self.kline_data = {}

    def login(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = Client(api_key, api_secret)
        self.bm = BinanceSocketManager(self.client)
        print("Logged in successfully.")

    def kline_handler(self, msg):
        symbol = msg['s']
        kline = msg['k']
        self.kline_data[symbol] = {
            'open': kline['o'],
            'high': kline['h'],
            'low': kline['l'],
            'close': kline['c'],
            'volume': kline['v'],
            'timestamp': kline['t']
        }
        print(f"Kline data for {symbol}: {self.kline_data[symbol]}")

    def start_kline_socket(self, symbol):
        # Correct WebSocket stream type and method
        self.bm.start_kline_socket(symbol, self.kline_handler, interval=Client.KLINE_INTERVAL_1MINUTE)

    def start(self):
        self.bm.start()

    def stop(self):
        # Stop all sockets
        self.bm.close()

    def get_account_info(self):
        if self.client:
            account_info = self.client.get_account()
            return account_info
        else:
            print("Please login first.")
            return None

if __name__ == "__main__":
    api_key = '88e262c5697a9971f573a9c078d0956ad1bc5fb77a81eeae535952c8f8635637'
    api_secret = 'b27ce9a1ee11b3cad52b1a7248222feb1394c39c3896fb1c9868ded2bf3a1a6e'

    broker = Broker()
    
    # Log in to the broker
    broker.login(api_key, api_secret)

    # Get account information
    account_info = broker.get_account_info()
    if account_info:
        print(json.dumps(account_info, indent=4))

    # List of stock symbols
    stocks = [
        'AAPL'
    ]

    # Binance uses different symbols for these stocks in its market, typically ending with 'USDT' for USD Tether trading pairs.
    binance_symbols = [stock + 'USDT' for stock in stocks]

    # Start WebSocket for each stock symbol
    for symbol in binance_symbols:
        broker.start_kline_socket(symbol)

    # Start the BinanceSocketManager
    broker.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        broker.stop()
        print("Stopped.")
