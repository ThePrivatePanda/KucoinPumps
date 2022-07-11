import time
import base64
import hmac
import hashlib
import requests
import random
import json

api_key = ""
api_secret = ""
api_passphrase = ""
passphrase = ""
url = "https://api.kucoin.com/api/v1/accounts/transferable?currency=LUNA&type=TRADE"

def get_balance():
    now = int(time.time() * 1000)
    str_to_sign = str(now) + "GET" + "/api/v1/accounts/transferable?currency=LUNA&type=TRADE"
    signature = base64.b64encode(
        hmac.new(
            api_secret.encode("utf-8"), str_to_sign.encode("utf-8"), hashlib.sha256
        ).digest()
    )
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
    }
    response = requests.get(url=url, headers=headers)
    resjso = response.json()
    return resjso["data"]["available"]

def sell_coin(amount):
    endpoint = "/api/v1/orders"
    payload = {
        "clientOid": str(random.randint(0, 1000)),
        "side": "sell",
        "symbol": "LUNA-USDT",
        "price": "0.00018",
        "size": amount,
        "type": "limit",
    }
    data = json.dumps(payload)
    now = str(int(time.time() * 1000))
    str_to_sign = f"{now}POST{endpoint}{data}"

    signature = base64.b64encode(
        hmac.new(
            api_secret.encode(
                "utf-8"), str_to_sign.encode("utf-8"), hashlib.sha256
        ).digest()
    )

    headers = {
        "KC-API-SIGN": signature.decode("utf-8"),
        "KC-API-TIMESTAMP": now,
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
    }
    response = requests.post(url=f"https://api.kucoin.com{endpoint}", headers=headers, json=payload)
    return (response.json())

while True:
    balance = get_balance()
    if float(balance) > 775000:
        sell_coin(round(float(balance), 4))

    time.sleep(10)
