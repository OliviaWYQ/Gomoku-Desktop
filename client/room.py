import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from showchessboard import *
import requests
import websocket

START_SIGNAL = -1
GUEST_READY_SIGNAL = -2
GUEST_UNREADY_SIGNAL = -3
GUEST_LEAVE_SIGNAL = -4
MASTER_DELETE_SIGNAL = -5
END_SIGNAL = -6

class GameRoomWindow(QWidget):
    def __init__(self, roomName, userName, serverIp, isMaster):
        super().__init__()
        self.layout = QHBoxLayout()
        self.roomName = roomName
        self.serverIp = serverIp
        self.userName = userName
        self.isMaster = isMaster

        self.title = "Game Hall"
        self.top = 100
        self.left = 100
        self.width = 600
        self.height = 200

        self.InitUI()
        self.initSocket()

    def InitUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.colors = QComboBox(self)
        self.colors.addItems(["Balck", "White"])
        self.colors.setGeometry(250, 40, 100, 20)
        self.colors.setEnabled(self.isMaster)

        self.startButton = QPushButton('Start', self)
        self.startButton.move(400, 34)
        self.startButton.clicked.connect(self.handleStart)
        self.startButton.setEnabled(self.isMaster)

        self.leaveButton = QPushButton('Leave', self)
        self.leaveButton.move(250, 94)
        self.leaveButton.clicked.connect(self.handleLeave)

        self.readyButton = QPushButton('Ready', self)
        self.readyButton.move(400, 94)
        self.readyButton.clicked.connect(self.handleReady)
        self.readyButton.setEnabled(not self.isMaster)

        self.show()

    def initSocket(self):
        # server location
        # should be 'ws://theIpOfServer:8080/playing'
        # '/test' is just for test 
        self.uri = 'ws://' + self.serverIp + ':8080/test'
        #uri = 'ws://' + self.serverIp + ':8080/playing'
        # role can be: "m" for master, "g" for guest, "a" for audience
        # if master use balck stone, "masterStone:1", if white, "masterStone:2"
        if self.colors.currentText() == 'Black':
            masterStone = '1'
        else:
            masterStone = '2'
        if self.isMaster:
            role = 'm'
        else:
            role = 'g'

        self.header = ["role:"+role, "roomName:"+self.roomName, "userName"+self.userName, "masterStone:"+masterStone]
        print(self.header)

        websocket.enableTrace(True)
        self.ws = websocket.WebSocket()
        self.ws.connect(self.uri,
                header=self.header)
        self.ws.on_message = self.on_message

    def on_message(self, ws, message):
        print('got')
        print(message)
        self.close()



    @pyqtSlot()
    def handleStart(self):
        self.ws.send("start")
        # trigger = Trigger(uri=uri, header=header)

        # # for test
        # # modify with pyqt
        # loop = asyncio.get_event_loop()
        # tasks = [onClick(trigger)]
        # loop.run_until_complete(asyncio.wait(tasks))

    @pyqtSlot()
    def handleLeave(self):
        # payload = {}
        # payload["master"] = self.userName.text()
        # payload["roomName"] = self.pwd.text()

        # result = requests.post('http://' + self.serverIp.text() + ':8080/auth/login', json=payload)
        
        # self.room = Room(self.userName.text(), self.serverIp.text())
        # self.room.show()
        # self.close()
        
        # TODO
        QMessageBox.warning(self, 'Error', 'Not implemented yet.')

    @pyqtSlot()
    def handleReady(self):
        # payload = {}
        # payload["master"] = self.userName.text()
        # payload["roomName"] = self.pwd.text()

        # result = requests.post('http://' + self.serverIp.text() + ':8080/auth/login', json=payload)
        
        # self.room = Room(self.userName.text(), self.serverIp.text())
        # self.room.show()
        # self.close()
        
        # TODO
        QMessageBox.warning(self, 'Error', 'Not implemented yet.')


########################### Create Room  ##############################

class CreateRoomWindow(QWidget):
    def __init__(self, masterName, serverIp):
        super().__init__()
        self.serverIp = serverIp
        self.masterName = masterName

        self.title = "Create a room"
        self.top = 100
        self.left = 100
        self.width = 600
        self.height = 300
        
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.createButton = QPushButton('Create', self)
        self.createButton.move(100, 180)
        self.createButton.clicked.connect(self.handleCreate)

        self.createButton = QPushButton('Back', self)
        self.createButton.move(200, 180)
        self.createButton.clicked.connect(self.handleBack)

        self.roomName = QLineEdit("Enter the room name", self)
        self.roomName.setGeometry(100, 100, 400, 30)

        self.show()

    @pyqtSlot()
    def handleBack(self):
        self.hallFromCreate = GameHallWindow(self.masterName, self.serverIp)
        self.hallFromCreate.show()
        self.close()
    
    @pyqtSlot()
    def handleCreate(self):

        payload = {}
        payload["master"] = self.masterName
        payload["roomName"] = self.roomName.text()

        result = requests.post('http://' + self.serverIp + ':8080/room', json=payload)
        
        if(result.text == "Success"):
            self.gameRoom = GameRoomWindow(self.roomName.text(), self.masterName, self.serverIp, True)
            self.gameRoom.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Error', result.text)




    
