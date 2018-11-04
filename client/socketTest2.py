import asyncio
import websockets
import time

async def hello(uri, header, timeout):
    async with websockets.connect(uri, extra_headers=header) as ws:
        flag = ""
        print("pas")
        flag = await ws.recv()
        print(f"< {flag}")
        flag = await ws.recv()
        print(f"< {flag}")
        time.sleep(5)
        for i in range(5):
            print(i)
            await ws.send(str(131072+i))
        time.sleep(timeout)
        ws.close()

asyncio.get_event_loop().run_until_complete(hello('ws://localhost:8080/playing', {"role": "g", "gameid":"123#456", "userName":"456", "masterStone":"1"}, 40))
