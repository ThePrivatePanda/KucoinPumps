import time
import base64
import hmac
import hashlib
import requests

api_key = ""
api_secret = ""
api_passphrase = ""
account_id = ""
base = "https://api.kucoin.com"


def get_account_balance():
    endpoint = f"/api/v1/accounts/{account_id}"
    now = str(int(time.time() * 1000))
    str_to_sign = f"{now}GET{endpoint}"
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
    response = requests.get(url=base + endpoint, headers=headers)
    return int(response.json()["data"]["available"].split(".")[0])


funds = get_account_balance()
funds = str(int(funds * (4 / 5)))
print(funds)
