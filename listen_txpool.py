import json

import websockets
import asyncio

from settings import Settings


async def subscribe(tx_status: str, url: str, api_key: str):
    print(url)
    async with websockets.connect(url + api_key) as ws:
        subscription_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "eth_subscribe",
            "params": [f"alchemy_{tx_status}Transactions"]
        }
        await ws.send(json.dumps(subscription_request))

        while True:
            msg = await ws.recv()
            print(json.loads(msg))


settings = Settings()
asyncio.get_event_loop().run_until_complete(subscribe(settings.TX_STATUS, settings.WEBSOCKET_URL, settings.API_KEY))
