import asyncio
import random
import aiohttp
from main import main
from internal import Message
import json

config = json.load(open("config.json"))
async def beat_the_damn_heart(ws):
    await ws.send_json({"op": 1, "d": None})

async def heartbeat(heartbeat_interval, ws):
    while True:
        await asyncio.sleep(heartbeat_interval)
        await beat_the_damn_heart(ws)
        print("---")

async def shutdown(ws, h):
    await ws.close()
    h.cancel()

async def start(token, extra=None):
    ws = await aiohttp.ClientSession().ws_connect(url="wss://gateway.discord.gg/?v=9&encoding=json")
    print("Connected")

    hello_res = (await ws.receive()).json()
    print("Received a hello.")

    heartbeat_interval = hello_res["d"]["heartbeat_interval"]/1000
    print("Base Heartbeat Interval:", heartbeat_interval)

    jitter_heartbeat = heartbeat_interval * random.uniform(0, 0.1)
    print("Sleeping for Jitter Heartbeat:", jitter_heartbeat)

    await asyncio.sleep(jitter_heartbeat)
    print("Sending heartbeat...")

    await beat_the_damn_heart(ws)
    print("We should get OP 0 with session_id in a few seconds, or OP 11.")

    msg = await ws.receive()
    msg_json = msg.json()

    if msg_json["t"] == "SESSIONS_REPLACE":
        session_id = msg_json["d"][0]["session_id"]
        print("Got Session ID:", session_id)
        print("We should get OP 11 in a few seconds.")
        msg = await ws.receive()
        print(msg.json())

    print("Successful, identifying now.")
    await ws.send_json(
        {
            "op": 2, 
            "d": {
                "token": token, 
                "intents": 37377, 
                "properties": {
                    "$os": "windows", 
                    "$browser": "Discord", 
                    "$device": "desktop"
                }
            }
        }
    )

    h = asyncio.ensure_future(heartbeat(heartbeat_interval, ws))
    res = await ws.receive()

    print("Received data")
    print(res.data)
    res = res.json()

    if res.get('t') == 'READY':
        session_id = res['d']['session_id']
        print("Got Session ID:", session_id)
        print("----------------------READY----------------------")
    else:
        raise SystemExit

    if not extra:
        return ws, session_id, h

    await ws.send_json(extra)
    msg = await ws.receive()
    msg_json = msg.json()
    if msg_json["t"] == "SESSIONS_REPLACE":
        session_id = msg_json["d"][0]["session_id"]
        print("Got Session ID:", session_id)
        msg = await ws.receive()
        msg_json = msg.json()

    msg = await ws.receive()
    print(msg.data)
    msg_json = msg.json()
    if msg_json["d"] == {}:
        return ws, session_id, h
    else:
        print("Resume failed, I can't handle it anymore man, I give up.")
        raise SystemExit

async def buff(token):
    ws, session_id, h = await start(token)
    await listen(token, ws, session_id, h)

async def listen(token, ws, session_id, h):
    while True:
        res = await ws.receive()
        jso = res.json()
        seq = jso['s']
        if jso["op"] == 1:
            print("Discord request an instance heartbeat, sending...")
            await beat_the_damn_heart(ws)
            continue
        if jso["op"] == 7:
            await shutdown(ws, h)
            await start(token, {"op": 6, "d": {"token": token, "session_id": session_id, "seq": seq}})
            return

        # now we can do what we want hehe
        try:
            if jso:
                if jso["d"] != 11:
                    await main(Message(jso["d"]))
        except Exception as e:
            print(e)


asyncio.get_event_loop().run_until_complete(buff(config["token"]))
