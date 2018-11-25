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
        await ws.send(str(529))
        flag = await ws.recv()
        print(f"< {flag}")

        flag = await ws.recv()
        print(f"< {flag}")
        await ws.send(str(1570))
        flag = await ws.recv()
        print(f"< {flag}")

        flag = await ws.recv()
        print(f"< {flag}")
        await ws.send(str(2628))
        flag = await ws.recv()
        print(f"< {flag}")

        flag = await ws.recv()
        print(f"< {flag}")
        await ws.send(str(3720))
        flag = await ws.recv()
        print(f"< {flag}")

        # flag = await ws.recv()
        # print(f"< {flag}")
        # await ws.send(str(4812))
        # flag = await ws.recv()
        # print(f"< {flag}")
        
        time.sleep(timeout)
        ws.close()

asyncio.get_event_loop().run_until_complete(hello('ws://localhost:8080/playing', {"role": "g", "roomName":"123#456", "userName":"456", "masterStone":"1"}, 40))
