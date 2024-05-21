# The REST baseurl for testnet is "https://testnet.binancefuture.com"
# The Websocket baseurl for testnet is "wss://fstream.binancefuture.com"

import requests

base_url="https://testnet.binancefuture.com"
stocks = [
    'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'BRK-A', 'BRK-B', 'JPM', 'JNJ',
    'V', 'WMT', 'PG', 'NVDA', 'MA', 'DIS', 'UNH', 'HD', 'PYPL', 'BAC', 
    'CMCSA', 'INTC', 'ADBE', 'ASML', 'NFLX', 'TSM', 'KO', 'PFE', 'PEP', 'VZ'
]
paratameters={
        "symbol" : stocks,
        "interval": "1h"
    }   
#trying 
def getdata():
    req=requests.get(url="https://testnet.binancefuture.com/fapi/v1/klines",params=paratameters)
    print(req.json())
    test=req.json()
# only accessing the high lows open close
    for i in range(20):  # Assuming you want the first 20 entries
            for j in range(1, 5):
                print(test[i][j])
def buyorder():
     reqbuy=requests.get(url="https://testnet.binancefuture.com/fapi/v1/ticker/bookTicker", params=paratameters.get("symbol"))
     print(reqbuy.json())
     
     buyreq=requests.
     
def recenttradelist():
    reqrecent=requests.get(url="https://testnet.binancefuture.com/fapi/v1/trades",params=paratameters.get("symbol"))
    return reqrecent
def pricetracker():
    
    
