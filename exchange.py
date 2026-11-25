import requests 
import json
import time
import logging
from dotenv import load_dotenv
import os
from symbols import SYMBOLS

logger = logging.getLogger(__name__)

load_dotenv()
interval = os.getenv("RETRY_INTERVAL")
timeout = os.getenv("FETCH_TIMEOUT")

def fetch_json(exchange, url, params=None, retries=3, interval= int(interval)):
    while retries != 0:
        try:
            r = requests.get(url, params=params, timeout=int(timeout))
            r.raise_for_status()

            data = r.json()
            return data
        
        except Exception as err:
            
            retries -= 1

            if retries == 0:
                raise
            logger.warning(f'{exchange} fetch was unsuccessful, retrying... {retries} left | Reason: {err}')
            time.sleep(interval)
            interval += 1
    

def get_binance_prices():

    data = fetch_json("binance",'https://api.binance.com/api/v3/ticker/price', 
    {"symbols": json.dumps(SYMBOLS, separators=(',', ":"))})
    
    return data

def get_bybit_prices():

    data  = fetch_json("bybit",'https://api.bybit.com/v5/market/tickers?category=spot')

    if data["retCode"] != 0:
        raise ValueError(f'bybit API error: {data["retMsg"]}', )
    
    lists = data["result"]["list"]
    prices = []

    for sym in lists:
        if sym["symbol"] in SYMBOLS:
            prices.append({"symbol":sym["symbol"], "price": sym["lastPrice"]})

    return prices

def get_okx_prices():

    data = fetch_json("okx",'https://openapi.okx.com/api/v5/market/tickers?instType=SPOT')

    if data["code"] != "0":
        raise ValueError(f'okx API error: {data["msg"]}')
    lists = data["data"]

    prices = []
    for sym in lists:
        sym["instId"] = sym["instId"].replace("-","")
        if sym["instId"] in SYMBOLS:
            prices.append({"symbol":sym["instId"], "price":sym["last"]})

    return prices