import json
import time
import aiohttp
import asyncio
import threading

async def heartbeat(ws):
    await ws.send_json(json.dumps({"op": 1, "d": None}))

def beatheart(ws, heartbeat_interval):
    while True:
        time.sleep(heartbeat_interval/1000)
        asyncio.run(heartbeat(ws))

async def connect(token):
    ws = await aiohttp.ClientSession().ws_connect(url="wss://gateway.discord.gg/?v=9&encoding=json")
    RECV = (await ws.receive()).json()
    await ws.send_json(
            {
                "op":2,
                "d": {
                    "token": token,
                    "intents": 4609,
                    "properties": {
                        "$os":"windows",
                        "$browser":"Discord",
                        "$device": "desktop"
                    }
                }
            }
        )

    # await ws.send_json(json.dumps({"op":2,"d": {"token":token, "intents": 1, "properties": {"$os":"linux","$browser":"nextcord==2.0.0a8","$device": "nextcord==2.0.0a8" }}}))

    heartbeat_interval = RECV['d']['heartbeat_interval']

    threading.Thread(target=beatheart, args=(ws, heartbeat_interval)).start()
    while True:
        try:
            msg = await ws.receive()
            if msg:
                print(msg.data)
        except KeyboardInterrupt:
            raise SystemExit
        except:
            pass

asyncio.run(connect("discord_token"))
