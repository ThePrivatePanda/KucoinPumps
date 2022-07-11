import time
import base64
import hmac
import hashlib
import requests
import uuid
import json

api_key = ""
api_secret = ""
api_passphrase = ""
base = "https://api.kucoin.com"


def buy(coin, usdt):
    endpoint = "/api/v1/orders"
    payload = {
        "clientOid": str(uuid.uuid4()).replace("-", ""),
        "side": "buy",
        "funds": usdt,
        "symbol": f"{coin}-USDT",
        "type": "market",
    }
    print(payload["funds"])

    data = json.dumps(payload)
    now = str(int(time.time() * 1000))
    str_to_sign = f"{now}POST{endpoint}{data}"
    signature = base64.b64encode(
        hmac.new(
            api_secret.encode("utf-8"), str_to_sign.encode("utf-8"), hashlib.sha256
        ).digest()
    )
    passphrase = base64.b64encode(
        hmac.new(
            api_secret.encode("utf-8"), api_passphrase.encode("utf-8"), hashlib.sha256
        ).digest()
    )
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": now,
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
    }
    response = requests.post(url=f"{base}{endpoint}", headers=headers, json=payload)
    print(response)
    print(response.content)
    return response.json()["data"]["orderId"]


print(buy("DOGE", 1))
