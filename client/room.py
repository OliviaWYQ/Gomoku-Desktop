import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from showchessboard import *
import requests

from ws4py.client.threadedclient import WebSocketClient

START_SIGNAL = -1
GUEST_READY_SIGNAL = -2
GUEST_UNREADY_SIGNAL = -3
GUEST_LEAVE_SIGNAL = -4
MASTER_DELETE_SIGNAL = -5
END_SIGNAL = -6

START_SIGNAL_MESSAGE = '-1'
GUEST_READY_SIGNAL_MESSAGE = '-2'
GUEST_UNREADY_SIGNAL_MESSAGE = '-3'
GUEST_LEAVE_SIGNAL_MESSAGE = '-4'
MASTER_DELETE_SIGNAL_MESSAGE = '-5'
END_SIGNAL_MESSAGE = '-6'

class socketCli(WebSocketClient):
    def hook(self, toInfluence):
        self.toInfluence = toInfluence

    def opened(self):
        #self.send("open")
        pass
 
    def closed(self, code, reason=None):
        print("Closed down", code, reason)
 
    def received_message(self, message):
        self.toInfluence.handleMessage(message.data.decode("utf-8"))

class GameRoomWindow(QWidget):
    def __init__(self, roomName, masterName, guestName, serverIp, isMaster, backHook):
        super().__init__()

        self.backHook = backHook

        self.layout = QHBoxLayout()
        self.roomName = roomName
        self.serverIp = serverIp
        #self.userName = userName
        self.isMaster = isMaster

        self.masterName = masterName
        self.guestName = guestName

        self.title = "Game Hall"
        self.top = 100
        self.left = 100
        self.width = 600
        self.height = 200

        self.ready = False

        self.initUI()
        self.initSocket()

    def initUI(self):
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

        self.readyButton = QPushButton('Unready', self)
        self.readyButton.move(400, 94)
        self.readyButton.clicked.connect(self.handleReady)
        self.readyButton.setEnabled(not self.isMaster)

        self.show()

    def handleMessage(self, message):
        print("Received: ", message)
        if message[0] == 'J':
            # join signal
            if self.isMaster:
                self.guestName = message[1:]
        else:
            try:
                signal = int(message)
                if signal < 0:
                    # START_SIGNAL = -1
                    # GUEST_READY_SIGNAL = -2
                    # GUEST_UNREADY_SIGNAL = -3
                    # GUEST_LEAVE_SIGNAL = -4
                    # MASTER_DELETE_SIGNAL = -5
                    # END_SIGNAL = -6
                    
                    if self.isMaster:
                        print(signal)
                        if signal == GUEST_READY_SIGNAL:
                            print("ready")
                            self.ready = True
                            self.readyButton.setText("Ready")
                        elif signal == GUEST_UNREADY_SIGNAL:
                            print("unready")
                            self.ready = False
                            self.readyButton.setText("Unready")
                        elif signal == GUEST_LEAVE_SIGNAL:
                            self.ready = False
                            self.readyButton.setText("Unready")
                            self.guestName = None
                        else:
                            print("Unvalid master control signal.")
                    else:
                        pass
                    # control signal
                else:
                    # should not be processed now
                    print("Moving signal, we are not start yet.")
            except:
                print("Unvalid message format.")


    def initSocket(self):
        self.uri = 'ws://' + self.serverIp + ':8080/playing'
        # self.uri = 'ws://' + self.serverIp + ':8080/test'
        # uri = 'ws://' + self.serverIp + ':8080/playing'
        # role can be: "m" for master, "g" for guest, "a" for audience
        # if master use balck stone, "masterStone:1", if white, "masterStone:2"
        if self.colors.currentText() == 'Black':
            masterStone = '1'
        else:
            masterStone = '2'

        if self.isMaster:
            role = 'm'
            userName = self.masterName
        else:
            role = 'g'
            userName = self.guestName
            
        self.headers = [("role", role), 
            ("roomName", self.roomName),
            ("userName", userName),
            ("masterStone", masterStone)]
        self.ws = socketCli(self.uri, headers=self.headers)
        self.ws.connect()
        self.ws.hook(self)
        # self.ws.send("my test...")
        # self.ws.run_forever()

    @pyqtSlot()
    def handleStart(self):
        #self.ws.send("start")
        pass

    @pyqtSlot()
    def handleLeave(self):
        # TODO: we need to send info to redis
        print ("we need to send info to redis")
        # payload = {}
        # payload["master"] = self.userName.text()
        # payload["roomName"] = self.pwd.text()
        # result = requests.post('http://' + self.serverIp.text() + ':8080/auth/login', json=payload)
        if self.isMaster:
            pass
        else:
            reply = QMessageBox.question(self, 'Exit', 'You sure to exit?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.ws.send(GUEST_LEAVE_SIGNAL_MESSAGE)
                self.backHook()
                self.close()


    @pyqtSlot()
    def handleReady(self):
        # TODO: we need to send info to redis
        print ("we need to send info to redis")
        # payload = {}
        # payload["master"] = self.userName.text()
        # payload["roomName"] = self.pwd.text()
        # result = requests.post('http://' + self.serverIp.text() + ':8080/auth/login', json=payload)
        
        if self.ready:
            self.ready = False
            self.ws.send(GUEST_UNREADY_SIGNAL_MESSAGE)
            self.readyButton.setText("Unready")
        else:
            self.ready = True
            self.ws.send(GUEST_READY_SIGNAL_MESSAGE)
            self.readyButton.setText("Ready")



########################### Create Room  ##############################

class CreateRoomWindow(QWidget):
    def __init__(self, masterName, serverIp, backHook):
        super().__init__()

        self.backHook = backHook
        self.serverIp = serverIp
        self.masterName = masterName

        self.title = "Create a room"
        self.top = 100
        self.left = 100
        self.width = 600
        self.height = 300
        
        self.initUI()

    def initUI(self):
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
        self.backHook()
        self.close()
    
    @pyqtSlot()
    def handleCreate(self):
        payload = {}
        payload["master"] = self.masterName
        payload["roomName"] = self.roomName.text()

        result = requests.post('http://' + self.serverIp + ':8080/room', json=payload)
        
        if(result.text == "Success"):
            self.gameRoom = GameRoomWindow(self.roomName.text(), self.masterName, None, self.serverIp, True, self.backHook)
            self.gameRoom.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Error', result.text)

    
