import requests 

try:

    r = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT', timeout = 10)

    r.raise_for_status()

    data = r.json()

    symbol = data["symbol"]
    price = data["price"]
    
    print(price, type(price))
except requests.exceptions.HTTPError as http_err:
    print(f'HTTP error occured: {http_err}')
except requests.exceptions.RequestException as err:
    print(f'Other error occured: {err}')
