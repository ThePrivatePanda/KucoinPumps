from discord.ext import commands
import time
import base64
import hmac
import hashlib
import math
import requests
import uuid
import json
import time
import single_functions.config as config

bot = commands.Bot(command_prefix=".", help_command=None)
base = "https://api.kucoin.com"


def buy(coin: str, usdt: str) -> str:
    endpoint = "/api/v1/orders"
    payload = {
        "clientOid": str(uuid.uuid4()).replace("-", ""),
        "side": "buy",
        "funds": usdt,
        "symbol": f"{coin.upper()}-USDT",
        "type": "market",
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
    passphrase = base64.b64encode(
        hmac.new(
            api_secret.encode(
                "utf-8"), api_passphrase.encode("utf-8"), hashlib.sha256
        ).digest()
    )
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": now,
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
    }
    response = requests.post(
        url=f"{base}{endpoint}", headers=headers, json=payload)
    print(response.content)
    return response.json()["data"]["orderId"]


def get_order(orderId, full=False):
    endpoint = f"/api/v1/orders/{orderId}"
    payload = {
        "orderId": orderId,
    }
    data = json.dumps(payload)
    now = str(int(time.time() * 1000))
    str_to_sign = f"{now}GET{endpoint}{data}"
    signature = base64.b64encode(
        hmac.new(
            api_secret.encode(
                "utf-8"), str_to_sign.encode("utf-8"), hashlib.sha256
        ).digest()
    )
    passphrase = base64.b64encode(
        hmac.new(
            api_secret.encode(
                "utf-8"), api_passphrase.encode("utf-8"), hashlib.sha256
        ).digest()
    )
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": now,
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
    }
    response = requests.get(
        url=f"{base}{endpoint}", headers=headers, json=payload)
    print(response.json())

    if full:
        return response.json()
    else:
        return response.json()["data"]["dealSize"]


def get_symbol(coin):
    endpoint = f"/api/v1/symbols"
    now = str(int(time.time() * 1000))
    str_to_sign = f"{now}GET{endpoint}"
    signature = base64.b64encode(
        hmac.new(
            api_secret.encode(
                "utf-8"), str_to_sign.encode("utf-8"), hashlib.sha256
        ).digest()
    )
    passphrase = base64.b64encode(
        hmac.new(
            api_secret.encode(
                "utf-8"), api_passphrase.encode("utf-8"), hashlib.sha256
        ).digest()
    )
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": now,
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
    }
    response = requests.get(url=f"{base}{endpoint}", headers=headers)
    jso = response.json()["data"]
    for i in jso:
        if i["symbol"] == f"{coin}-USDT":
            print(i)
            return i["baseIncrement"]


def calc_sell_price(invested: str, coin_bought: str, avg_expected_gain: str) -> float:
    avg_price = float(invested) / float(coin_bought)
    profit = (float(avg_expected_gain) / 100) * avg_price
    saleprice = math.ceil(float(invested) + float(profit))
    return saleprice


def sell(coin: str, coin_bought: str, resale_price: str):
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
            api_secret.encode(
                "utf-8"), str_to_sign.encode("utf-8"), hashlib.sha256
        ).digest()
    )
    passphrase = base64.b64encode(
        hmac.new(
            api_secret.encode(
                "utf-8"), api_passphrase.encode("utf-8"), hashlib.sha256
        ).digest()
    )
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": now,
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
    }
    response = requests.post(
        url=f"{base}{endpoint}", headers=headers, json=payload)
    print(response.content)
    return response.json()["data"]["orderId"]


@bot.listen("on_message")
async def pump(message):
    before = time.time()
    if message.channel.id not in (872223192838705242, 929760015336734790):
        return
    if message.author.id not in (
        815347746974072852,
        736147895039819797,
        763246477773766697,
    ):
        return
    if not (
        "Coin is" in message.content
        and "%" in message.content
        and "https://trade.kucoin.com/" in message.content
    ):
        return

    investment = "100"
    coin = message.content.split("-")[0].split("/")[-1]
    orderId = buy(coin, investment)
    ints = [i for i in message.content if i.isdigit()]
    if len(ints) == 6:
        minimum_expected_gain = int("".join(ints[:3]))
        maximum_expected_gain = int("".join(ints[3:]))
        avg_expected_gain = str(
            (float(minimum_expected_gain) + float(maximum_expected_gain)) / 2
        )
    elif len(ints) == 7:
        minimum_expected_gain = int("".join(ints[:3]))
        maximum_expected_gain = int("".join(ints[4:]))
        avg_expected_gain = str(
            (float(minimum_expected_gain) + float(maximum_expected_gain)) / 2
        )
    elif len(ints) == 8:
        minimum_expected_gain = int("".join(ints[:4]))
        maximum_expected_gain = int("".join(ints[4:]))
        avg_expected_gain = str(
            (float(minimum_expected_gain) + float(maximum_expected_gain)) / 2
        )
    elif len(ints) in (3, 4):
        avg_expected_gain = int("".join(ints[4:])) - 100

    while True:
        coin_bought = get_order(orderId)
        if coin_bought != "0":
            break

    coin_bought_sell = f"{coin_bought.split('.')[0]}.{(coin_bought.split('.')[-1])[:-(len(coin_bought.split('.')[-1])-len(get_symbol(coin).split('.')[-1]))]}"
    sell_price = calc_sell_price(investment, coin_bought, avg_expected_gain)
    saleOrderId = sell(
        coin,
        coin_bought_sell,
        sell_price,
    )
    channel = bot.get_channel(929968743939993641)
    await channel.send(
        f"@everyone Bought `{coin_bought}` `{coin.upper()}` with an investment of `{investment}` USDT. Placed limit sell at `{sell_price*int(float(coin_bought))}` Expected gain is `{avg_expected_gain}%` and it took me `{time.time()-before}` to do it.\nThe sale order id is `{saleOrderId}` Check its status by `.status {saleOrderId}`"
    )


@bot.command(name="status")
async def status_(ctx, orderID):
    investment = 0
    content = "None"
    args = ctx.message.content.split(" ")
    if "full" in ctx.message.content or "all" in ctx.message.content:
        content = "all"
    for i in args:
        if i.isdigit():
            investment = int(i)

    if ctx.author.id not in (736147895039819797, 871607527849230346):
        return

    stuff = get_order(orderID, True)

    if not investment:
        if content == "all":
            await ctx.send(stuff)
        else:
            await ctx.send(f"Sold: {not stuff['data']['isActive']}")
    else:
        if content == "all":
            profit_on_sell = int(stuff["data"]["price"]) - investment
            await ctx.send(
                f"Expected profit is `{profit_on_sell}$` i.e. `{int(profit_on_sell/2)}$` each\n{stuff}"
            )
        else:
            profit_on_sell = int(stuff["data"]["price"]) - investment
            await ctx.send(
                f"Expected profit is `{profit_on_sell}$` i.e. `{int(profit_on_sell/2)}$` each\nSold: {not stuff['data']['isActive']}"
            )


bot.run(config.token)
