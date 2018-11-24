import asyncio
import time

from websocket import create_connection
import websocket

# function to handle the message received from server
def on_message(ws, message):
    print("got")

class Trigger:
    
    message = True
    click = True
    stop = False

    def __init__(self, uri, header):
        self.uri = uri
        self.header = header
        self.click = True
        self.stop = False

        # core(Line24 ~ 31), establish socket to server 
        websocket.enableTrace(True)
        self.ws = websocket.WebSocket()
        self.ws.connect(self.uri,
                header=self.header)
        print("connected")
        # handle message from server, on_message() is defined at the beginning
        self.ws.on_message = on_message

    # check whether we still need to handle click event
    # just for test, can ignore when implement real funciton 
    def handleClick(self):
        return self.click

    def shutDown(self):
        self.stop = True
        self.click = False
    
    def isRunning(self):
        return not self.stop

    # core, send message to server
    def send(self, message):
        self.ws.send(message)

# handle click event
# for test
# modify with pyqt
@asyncio.coroutine
def onClick(trigger):
    i = 0
    while(True and trigger.handleClick()):
        print(trigger.handleClick())
        trigger.send("test")
        yield from asyncio.sleep(1)
        i += 1
        if(i>5):
            print('close')
            trigger.shutDown()
    print(trigger.handleClick())

if __name__ == "__main__":
    # server location
    # should be 'ws://theIpOfServer:8080/playing'
    # '/test' is just for test 
    uri = 'ws://localhost:8080/test'
    # role can be: "m" for master, "g" for guest, "a" for audience
    # if master use balck stone, "masterStone:1", if white, "masterStone:2"
    header = ["role:m", "roomName:aname", "userName:123", "masterStone:1"]

    trigger = Trigger(uri=uri, header=header)

    # for test
    # modify with pyqt
    loop = asyncio.get_event_loop()
    tasks = [onClick(trigger)]
    loop.run_until_complete(asyncio.wait(tasks))
