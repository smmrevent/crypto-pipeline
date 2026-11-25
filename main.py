from db import save_prices
from dotenv import load_dotenv
import psycopg
import os
from exchange import get_binance_prices, get_bybit_prices, get_okx_prices
import logging
import time

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")

logger = logging.getLogger(__name__)

exchanges = [("binance", get_binance_prices),
             ("bybit", get_bybit_prices),
             ("okx", get_okx_prices),]

load_dotenv()

dbname = os.getenv('POSTGRES_NAME')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv("POSTGRES_HOST")
interval = os.getenv("GATHER_INTERVAL")

with psycopg.connect(dbname=dbname, user=user, password=password, host=host) as conn:
    while True:
        for exchange, fetch in exchanges:
            try:
                ticker = fetch()
            except Exception as err:
                logger.error("Error occurred while fetching %s: %s", exchange, err)
                continue
            try:
                save_prices(ticker, exchange, conn)
            except Exception as err:
                logger.error("Error occurred while saving prices: %s", err)
        time.sleep(int(interval))
    