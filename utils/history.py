import time
import base64
import hmac
import hashlib
import requests
import json

api_key = ""
api_secret = ""
api_passphrase = ""
base_url = "https://api.kucoin.com"


def get_headers(method, endpoint, body=None):
    now = int(time.time() * 1000)
    if body:
        str_to_sign = str(now) + method + endpoint
    else:
        str_to_sign = str(now) + method + endpoint + json.dumps(body)

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

    return {
        "KC-API-KEY": api_key,
        "KC-API-KEY-VERSION": "2",
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
    }


def get_start_time():
    endpoint = f"/api/v1/market/candles?type=1min&symbol=BTC-USDT&startAt=1643352421643350300&endAt=1750000000"
    response = requests.get(
        url=base_url + endpoint,
        headers=get_headers("get", endpoint),
    )
    print(response.json())
    return int(response.json()["data"])


starttime = get_start_time()
# endttime = int(time.time())
# time_jumps = []
# for i in range(starttime, endttime, 90000):
#     time_jumps.append([i, i + 1])
# print(time_jumps)
