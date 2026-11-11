import requests 
import json
from symbols import SYMBOLS

def get_binance_prices():
    try:
        r = requests.get('https://api.binance.com/api/v3/ticker/price', 
        params={"symbols": json.dumps(SYMBOLS, separators=(',',':'))}, 
        timeout = 10)
        
        r.raise_for_status()

        data = r.json()

    except requests.HTTPError as err:
        print(f'HTTP error occured: {err}')
        raise
    except requests.ConnectionError as err:
        print(f'Connection error occured:{err}')
        raise
    except requests.RequestException as err:
        print(f'Other error occured: {err}')
        raise
    return data

def get_bybit_prices():
    try:
        r  = requests.get('https://api.bybit.com/v5/market/tickers?category=spot',
                          timeout = 10)

        r.raise_for_status()

        data = r.json()
        lists = data["result"]["list"]
        prices = []

        for sym in lists:
            if sym["symbol"] in SYMBOLS:
                prices.append({"symbol":sym["symbol"], "price": sym["lastPrice"]})

    except requests.HTTPError as err:
        print(f'HTTP error occured: {err}')
        raise
    except requests.ConnectionError as err:
        print(f'Connection error occured:{err}')
        raise
    except requests.RequestException as err:
        print(f'Other error occured: {err}')
        raise
    return prices

def get_okx_prices():
    try:   
        r = requests.get('https://openapi.okx.com/api/v5/market/tickers?instType=SPOT',
                        timeout = 10)
        r.raise_for_status()

        data = r.json()
        if data["code"] != "0":
            raise ValueError(f'OKX API error: {data["msg"]}')
        lists = data["data"]

        prices = []
        for sym in lists:
            sym["instId"] = sym["instId"].replace("-","")
            if sym["instId"] in SYMBOLS:
                prices.append({"symbol":sym["instId"], "price":sym["last"]})
    except requests.HTTPError as err:
        print(f'HTTP error occured: {err}')
        raise
    except requests.ConnectionError as err:
        print(f'Connection error occured:{err}')
        raise
    except requests.RequestException as err:
        print(f'Other error occured: {err}')
        raise
    return prices