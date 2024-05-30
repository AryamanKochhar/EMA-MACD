import requests
import pandas as pd
import numpy as np
import time
import hmac
import hashlib
class BinanceClient:
    def __init__(self, api_key, api_secret_key, base_url="https://testnet.binancefuture.com"):
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.base_url = base_url

    def generate_signature(self, query_string):
        return hmac.new(self.api_secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def login(self):
        endpoint = "/fapi/v2/account"
        timestamp = int(time.time() * 1000)
        params = {
            "timestamp": timestamp,
        }
        query_string = '&'.join([f"{key}={params[key]}" for key in params])
        signature = self.generate_signature(query_string)
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        params["signature"] = signature
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers, params=params)

        if response.status_code == 200:
            print("Login successful! API key is correct.")
            return True
        else:
            print("Login failed. Check your API key and secret.")
            print(response.json())
            return False

    def get_klines(self, symbol, interval='1h', limit=20):
        url = f"{self.base_url}/fapi/v1/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        response = requests.get(url, params=params)
        data = response.json()
        # Print only open, high, low, and close values
        # for entry in data:
        #     print(f"Open: {entry[1]}, High: {entry[2]}, Low: {entry[3]}, Close: {entry[4]}")
        print(data)

    def get_order_book(self, symbol):
        url = f"{self.base_url}/fapi/v1/ticker/bookTicker"
        params = {"symbol": symbol}
        response = requests.get(url, params=params)
        print(response.json())

    def get_recent_trades(self, symbol):
        url = f"{self.base_url}/fapi/v1/trades"
        params = {"symbol": symbol}
        response = requests.get(url, params=params)
        print(response.json())

    def place_order(self, symbol, side, type, quantity, price=None):
        url = f"{self.base_url}/fapi/v1/order"
        timestamp = int(time.time() * 1000)
        params = {
            "symbol": symbol,
            "side": side,
            "type": type,
            "quantity": quantity,
            "timestamp": timestamp,
        }
        if price is not None:
            params["price"] = price
            params["timeInForce"] = "GTC"

        query_string = '&'.join([f"{key}={params[key]}" for key in params])
        signature = self.generate_signature(query_string)
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        params["signature"] = signature
        response = requests.post(url, headers=headers, params=params)
        print(response.json())

    def get_account_balance(self):
        endpoint = "/fapi/v2/balance"
        timestamp = int(time.time() * 1000)
        params = {
            "timestamp": timestamp,
        }
        query_string = '&'.join([f"{key}={params[key]}" for key in params])
        signature = self.generate_signature(query_string)
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        params["signature"] = signature
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers, params=params)
        print(response.json())

    def cancel_order(self, symbol, order_id):
        endpoint = "/fapi/v1/order"
        timestamp = int(time.time() * 1000)
        params = {
            "symbol": symbol,
            "orderId": order_id,
            "timestamp": timestamp,
        }
        query_string = '&'.join([f"{key}={params[key]}" for key in params])
        signature = self.generate_signature(query_string)
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        params["signature"] = signature
        response = requests.delete(f"{self.base_url}{endpoint}", headers=headers, params=params)
        print(response.json())

    def get_open_orders(self, symbol):
        endpoint = "/fapi/v1/openOrders"
        timestamp = int(time.time() * 1000)
        params = {
            "symbol": symbol,
            "timestamp": timestamp,
        }
        query_string = '&'.join([f"{key}={params[key]}" for key in params])
        signature = self.generate_signature(query_string)
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        params["signature"] = signature
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers, params=params)
        print(response.json())

    def get_all_orders(self, symbol, limit=20):
        endpoint = "/fapi/v1/allOrders"
        timestamp = int(time.time() * 1000)
        params = {
            "symbol": symbol,
            "timestamp": timestamp,
            "limit": limit,
        }
        query_string = '&'.join([f"{key}={params[key]}" for key in params])
        signature = self.generate_signature(query_string)
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        params["signature"] = signature
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers, params=params)
        print(response.json())

    def get_account_info(self):
        endpoint = "/fapi/v2/account"
        timestamp = int(time.time() * 1000)
        params = {
            "timestamp": timestamp,
        }
        query_string = '&'.join([f"{key}={params[key]}" for key in params])
        signature = self.generate_signature(query_string)
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        params["signature"] = signature
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers, params=params)
        print(response.json())

    def get_funding_rate(self, symbol, limit=20):
        endpoint = "/fapi/v1/fundingRate"
        params = {
            "symbol": symbol,
            "limit": limit
        }
        response = requests.get(f"{self.base_url}{endpoint}", params=params)
        print(response.json())

    def get_mark_price(self, symbol):
        endpoint = "/fapi/v1/premiumIndex"
        params = {"symbol": symbol}
        response = requests.get(f"{self.base_url}{endpoint}", params=params)
        print(response.json())

    def get_liquidation_orders(self, symbol, limit=20):
        endpoint = "/fapi/v1/allForceOrders"
        params = {
            "symbol": symbol,
            "limit": limit
        }
        response = requests.get(f"{self.base_url}{endpoint}", params=params)
        print(response.json())

    def get_income_history(self, limit=20):
        endpoint = "/fapi/v1/income"
        timestamp = int(time.time() * 1000)
        params = {
            "timestamp": timestamp,
            "limit": limit
        }
        query_string = '&'.join([f"{key}={params[key]}" for key in params])
        signature = self.generate_signature(query_string)
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        params["signature"] = signature
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers, params=params)
        print(response.json())

    def get_position_risk(self):
        endpoint = "/fapi/v2/positionRisk"
        timestamp = int(time.time() * 1000)
        params = {
            "timestamp": timestamp,
        }
        query_string = '&'.join([f"{key}={params[key]}" for key in params])
        signature = self.generate_signature(query_string)
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        params["signature"] = signature
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers, params=params)
        print(response.json())

    def get_commission_rate(self, symbol):
        endpoint = "/fapi/v1/commissionRate"
        params = {"symbol": symbol}
        response = requests.get(f"{self.base_url}{endpoint}", params=params)
        print(response.json())

    def change_leverage(self, symbol, leverage):
        endpoint = "/fapi/v1/leverage"
        timestamp = int(time.time() * 1000)
        params = {
            "symbol": symbol,
            "leverage": leverage,
            "timestamp": timestamp
        }
        query_string = '&'.join([f"{key}={params[key]}" for key in params])
        signature = self.generate_signature(query_string)
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        params["signature"] = signature
        response = requests.post(f"{self.base_url}{endpoint}", headers=headers, params=params)
        print(response.json())

if __name__ == "__main__":
    api_key = "88e262c5697a9971f573a9c078d0956ad1bc5fb77a81eeae535952c8f8635637"
    api_secret_key = "b27ce9a1ee11b3cad52b1a7248222feb1394c39c3896fb1c9868ded2bf3a1a6e"

    client = BinanceClient(api_key, api_secret_key)

    if client.login():
        symbol = "BTCUSDT"  # Example symbol
        client.get_klines(symbol)
        client.get_order_book(symbol)
        client.get_recent_trades(symbol)
        client.place_order(symbol, "BUY", "LIMIT", 0.01, 1000)
        client.get_account_balance()
        client.cancel_order(symbol, 12345678)
        client.get_open_orders(symbol)
        client.get_all_orders(symbol)
        client.get_account_info()
        client.get_funding_rate(symbol)
        client.get_mark_price(symbol)
        client.get_liquidation_orders(symbol)
        client.get_income_history()
        client.get_position_risk()
        client.get_commission_rate(symbol)
        client.change_leverage(symbol, 20)
    else:
        print("Cannot proceed without valid API credentials.")
#getting kline
