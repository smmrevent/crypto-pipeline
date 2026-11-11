import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

def get_prices():   
    with psycopg.connect(f"dbname=postgres user=postgres password={os.getenv('POSTGRES_PASSWORD')} host=localhost") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM prices")
            result = cur.fetchall()
            cur.close()
            conn.close()
            print(result)

def save_prices(data, exchange):
    with psycopg.connect(f"dbname=postgres user=postgres password={os.getenv('POSTGRES_PASSWORD')} host=localhost") as conn:
        with conn.cursor() as cur:
            rows = []
            for item in data:
                rows.append((exchange,item["symbol"], item["price"]))
            cur.executemany("INSERT INTO prices (ts, exchange, symbol, price) VALUES (NOW(), %s, %s, %s)", (rows))
            conn.commit()
            cur.close()
