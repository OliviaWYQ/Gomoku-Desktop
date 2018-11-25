import asyncio
import websockets
import time

async def hello(uri, header, timeout):
    async with websockets.connect(uri, extra_headers=header) as ws:
        flag = ""
        # await ws.send("""{"from":"123", "position":1}""")
        print("pas")
        flag = await ws.recv()
        print(f"< {flag}")
        while(flag != "end"):
            flag = await ws.recv()
            print(f"< {flag}")
        time.sleep(timeout)
        ws.close()

asyncio.get_event_loop().run_until_complete(hello('ws://localhost:8080/playing', {"role": "a", "roomName":"123#456", "userName":"777", "masterStone":"1"}, 20))