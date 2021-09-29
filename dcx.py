import requests as r
from hmac import new
from hashlib import sha256
from time import time, sleep
from json import dumps

key = ""
code = b""
url = ["https://public.coindcx.com", "https://api.coindcx.com"]

action = [["/market_data/trade_history", "/market_data/orderbook",  "/market_data/candles"], 
          ["/exchange/ticker", "/exchange/v1/markets", "/exchange/v1/markets_details",
          "/exchange/v1/users/balances", "/exchange/v1/users/info", "/exchange/v1/orders/create", "/exchange/v1/orders/create_multiple", "/exchange/v1/orders/status",
          "/exchange/v1/orders/status_multiple", "/exchange/v1/orders/active_orders", "/exchange/v1/orders/trade_history", "/exchange/v1/orders/active_orders_count",
          "/exchange/v1/orders/cancel_all", "/exchange/v1/orders/cancel_by_ids", "/exchange/v1/orders/cancel", "/exchange/v1/orders/edit"]]

coin = ["BTC", "ETH", "SOL", "ADA", "MATIC", "AAVE", "XRP", "ATOM"]

class order:
    def __init__(self, side, type_, market, quantity, rate):
        self.market, self.type_, self.side, self.quantity, self.rate = market, type_, side, quantity, rate
        return self


def tStamp():
    return int(round(time()*1000))


def sign(secr, js_body):
    # new() = hmac.new(), sha256 = hashlib.sha256
    return new(secr, js_body.encode(), sha256).hexdigest()


def header(sign):
    return {'Content-Type': 'application/json',
            'X-AUTH-APIKEY': key,
            'X-AUTH-SIGNATURE':sign}


def place_order(ord):
    body = {
        "side": ord.side,
        "type": ord.type_,
        "market": ord.market,
        "price_per_unit": ord.rate,
        "total_quantity": ord.quantity,
        "timeStap": tStamp()
    }
    # dumps() = json.dumps()
    js_body = dumps(body, separators=(",",":"))
    resp = r.post(url[0], data=js_body, headers=header(sign(code, js_body)))


def main():
    resp = r.get(url[0]+action[0][2]+"?pair=%s&interval=")

    body = {
        "timestamp":tStamp()
    }
    body = dumps(body)
    resp = r.post(url[1]+action[1][3], data=body, headers=header(sign(code, body)))
    data = resp.json()

    for d in data:
        if d['currency'] == 'INR':
            if float(d['balance']) >= 10.0:
                print(d['balance'])
            break

if __name__ == "__main__":
    main()
