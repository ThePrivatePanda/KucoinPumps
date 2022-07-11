import uuid, json, time, base64, hmac, hashlib, requests

api_key = ""
api_secret = ""
api_passphrase = ""
base = "https://api.kucoin.com"


def sell(coin, coin_bought, resale_price):
    endpoint = "/api/v1/orders"
    payload = {
        "clientOid": str(uuid.uuid4()).replace("-", ""),
        "side": "sell",
        "symbol": f"{coin}-USDT",
        "price": resale_price,
        "size": coin_bought,
        "type": "limit",
    }
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
    return response.json()["data"]["orderId"]


print(sell("", 0, 0))
