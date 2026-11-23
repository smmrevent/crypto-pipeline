from db import get_prices, save_prices
from exchange import get_binance_prices, get_bybit_prices, get_okx_prices
import time

exchanges = [("binance", get_binance_prices),
             ("bybit", get_bybit_prices),
             ("okx", get_okx_prices),]

while True:
    for exchange, fetch in exchanges:
        try:
            ticker = fetch()
            save_prices(ticker, exchange)
            print("Fetch was successful")
        except Exception as err:
           print(f'Something went wrong with {exchange} fetch: {err}, type: {type(err).__name__}')    
    time.sleep(60)
    