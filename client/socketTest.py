import asyncio
import websockets


async def hello(uri):
    async with websockets.connect(uri) as ws:
        flag = ""
        await ws.send("""{"from":"123", "position":1}""")
        print("pas")
        while(flag != "end"):
            flag = await ws.recv()
            print(f"< {flag}")
        ws.close()

asyncio.get_event_loop().run_until_complete(hello('ws://localhost:8080/playing'))