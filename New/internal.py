import re
import hashlib
import hmac
import base64
import json
import time
import asyncio
import aiohttp
import random

class Config:
    def __init__(self):
        self.config = json.load(open("config.json"))

    def update(self, key, value):
        self.config[key] = value
        json.dump(self.config, open("config.json", "w"))

    def get(self, key):
        return self.config.get(key, None)

class Message:
    def __init__(self, message_json) -> None:
        self.content = message_json["content"]
        self.channel_id = message_json["channel_id"]
        self.author_id = message_json["author"]["id"]

class Bot:
    def __init__(self) -> None:
        self.config = Config()

        self.investment = self.config.get("investment")
        self.api_key = self.config.get("api_key")
        self.api_secret = self.config.get("api_secret")
        self.api_passphrase = self.config.get("api_passphrase")
        self.passphrase = self.config.get("passphrase")
        self.token = self.config.get("token")

        self.base = "https://api.kucoin.com"

        self.reg = re.compile(
            r"^Coin is: [A-V]{1,10}\n\nhttps:\/\/trade.kucoin.com\/[A-V]{1,10}-USDT\n\nProjected Gain: [0-9]{2,10}-[0-9]{2,10}%$")

        self.session: aiohttp.ClientSession = asyncio.get_event_loop().run_until_complete(self.create_client_session())


    async def create_client_session(self):
        my_session = aiohttp.ClientSession()
        return my_session


    async def buy(self, coin: str, investment: int) -> str:
        endpoint = "/api/v1/orders"
        payload = {
            "clientOid": str(random.randint(0, 1000)),
            "side": "buy",
            "funds": str(investment),
            "symbol": f"{coin.upper()}-USDT",
            "type": "market",
        }

        data = json.dumps(payload)
        now = str(int(time.time() * 1000))
        str_to_sign = f"{now}POST{endpoint}{data}"

        signature = base64.b64encode(
            hmac.new(
                self.api_secret.encode(
                    "utf-8"), str_to_sign.encode("utf-8"), hashlib.sha256
            ).digest()
        )

        headers = {
            "KC-API-SIGN": signature.decode("utf-8"),
            "KC-API-TIMESTAMP": now,
            "KC-API-KEY": self.api_key,
            "KC-API-PASSPHRASE": self.passphrase,
            "KC-API-KEY-VERSION": "2",
        }

        response = await self.session.post(url=f"{self.base}{endpoint}", headers=headers, json=payload)
        return ((await response.json())["data"]["orderId"])

    async def sell(self, coin: str, coin_bought: str, resale_price: str):
        endpoint = "/api/v1/orders"
        payload = {
            "clientOid": str(random.randint(0, 1000)),
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
                self.api_secret.encode(
                    "utf-8"), str_to_sign.encode("utf-8"), hashlib.sha256
            ).digest()
        )

        headers = {
            "KC-API-SIGN": signature.decode("utf-8"),
            "KC-API-TIMESTAMP": now,
            "KC-API-KEY": self.api_key,
            "KC-API-PASSPHRASE": self.passphrase,
            "KC-API-KEY-VERSION": "2",
        }
        response = await self.session.post(url=f"{self.base}{endpoint}", headers=headers, json=payload)
        return (await response.json())["data"]["orderId"]

    async def get_order(self, orderId):
        endpoint = f"/api/v1/orders/{orderId}"
        payload = {
            "orderId": orderId,
        }
        data = json.dumps(payload)
        now = str(int(time.time() * 1000))
        str_to_sign = f"{now}GET{endpoint}{data}"
        signature = base64.b64encode(
            hmac.new(
                self.api_secret.encode(
                    "utf-8"), str_to_sign.encode("utf-8"), hashlib.sha256
            ).digest()
        )
        headers = {
            "KC-API-SIGN": signature.decode("utf-8"),
            "KC-API-TIMESTAMP": now,
            "KC-API-KEY": self.api_key,
            "KC-API-PASSPHRASE": self.passphrase,
            "KC-API-KEY-VERSION": "2",
        }

        response = await self.session.get(url=f"{self.base}{endpoint}", headers=headers, json=payload)
        return (await response.json())["data"]["dealSize"]


    async def send_message(self, channel_id, content):
        h = await self.session.post(
            url=f"https://discord.com/api/v9/channels/{channel_id}/messages",
            headers={
                "Authorization": self.token,
                "Content-Type": "application/json",
            },
            json={
                "content": content,
                "tts": False
            }
        )
        return h.status
