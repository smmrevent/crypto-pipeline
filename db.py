import logging

logger = logging.getLogger(__name__)

def save_prices(data, exchange, conn):
    with conn.transaction():
        with conn.cursor() as cur:
            rows = []
            for item in data:
                rows.append((exchange,item["symbol"], item["price"]))
            cur.executemany("INSERT INTO prices (ts, exchange, symbol, price) VALUES (NOW(), %s, %s, %s)", (rows))
    logger.info("Saved %d prices from %s", len(data), exchange)
