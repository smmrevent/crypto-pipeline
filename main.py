from db import get_prices, save_prices
from exchange import get_binance_prices, get_bybit_prices, get_okx_prices
import time

while True:
    binance_tickers = get_binance_prices()
    bybit_tickers = get_bybit_prices()
    okx_tickers = get_okx_prices()

    save_prices(binance_tickers, "binance")
    save_prices(bybit_tickers, "bybit")
    save_prices(okx_tickers, "okx")
    time.sleep(120)
    