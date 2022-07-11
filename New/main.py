import time
import json
from internal import Bot, Message
from symbols import symbols

bot = Bot()

config = json.loads(open("config.json").read())

async def main(message: Message):
    if message.content.startswith(".invest"):
        if message.channel_id == config.get("master_channel") and message.author_id == config.get("master_user"):
            investment_instead = int(message.content.split(" ")[1])
            bot.config.update("investment", investment_instead)
            bot.investment = investment_instead
            return await bot.send_message(config.get("master_channel"), f"Set investment to `{investment_instead}`.")

    if message.channel_id not in config.get("pump_signal_channels"):
        return False

    if not bot.reg.search(message.content):
        return False

    coin = message.content.split("-")[0].split("/")[-1]

    before = time.perf_counter()
    orderId = await bot.buy(coin, bot.investment)
    buy_time = time.perf_counter()

    while True:
        coin_bought_amount = await bot.get_order(orderId)
        if coin_bought_amount != "0":
            coin_bought_amount = coin_bought_amount
            break

    int1, int2 = message.content.split("Gain: ")[-1].split("%")[0].split("-")
    int1, int2 = int(int1), int(int2)
    avg_expected_gain = float((int1 + int2) / 2)

    coin_to_sell = f"{coin_bought_amount.split('.')[0]}.{(coin_bought_amount.split('.')[-1])[:-(len(coin_bought_amount.split('.')[-1])-len(symbols[coin].split('.')[-1]))]}"

    total_sell_price = bot.investment + \
        (avg_expected_gain/100) * bot.investment
    sell_price_per_coin = total_sell_price/float(coin_bought_amount)
    sell_price_per_coin = float(f"{sell_price_per_coin:.5f}")
    before_sell = time.time()
    await bot.sell(
        coin,
        coin_to_sell,
        sell_price_per_coin,
    )

    end = time.time()
    await bot.send_message(968915746241544262, 
        f"""
Coin Bought: `{coin_bought_amount}` {coin.upper()}
Sold at:
        Total: `{total_sell_price}`
        Per Coin: `{sell_price_per_coin}`
Invested: `{bot.investment}`
Profit: `{total_sell_price - bot.investment}`
Time Taken:
        Total: `{end - before}`
        Buy: `{buy_time - before}`
        Get Order: `{before_sell - buy_time}`
        Sell: `{before_sell - buy_time}`

        Start: `{before}`
        After Buy: `{buy_time}`
        After Get Order: `{before_sell}`
        After Sell: `{end}`
"""
    )
    await bot.send_message(config.get("master_channel"), "@everyone Done ^\n--------------------------------------")
