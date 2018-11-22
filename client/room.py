import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from showchessboard import *
import requests

class GameRoom(QWidget):
    def __init__(self, roomName, userName, serverIp):
        super().__init__()
        self.layout = QHBoxLayout()
        self.roomName = roomName
        self.serverIp = serverIp
        self.userName = userName

        self.title = "Game Hall"
        self.top = 100
        self.left = 100
        self.width = 600
        self.height = 200

        self.InitUI()
    
    def InitUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.colors = QComboBox(self)
        self.colors.addItems(["Balck", "White"])
        self.colors.setGeometry(250, 40, 100, 20)

        startButton = QPushButton('Start', self)
        startButton.move(400, 34)
        startButton.clicked.connect(self.handleStart)

        leaveButton = QPushButton('Leave', self)
        leaveButton.move(250, 94)
        leaveButton.clicked.connect(self.handleLeave)

        readyButton = QPushButton('Ready', self)
        readyButton.move(400, 94)
        readyButton.clicked.connect(self.handleReady)

        self.show()


    @pyqtSlot()
    def handleStart(self):
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

class CreateRoom(QWidget):
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

        createButton = QPushButton('Create', self)
        createButton.move(100, 180)
        createButton.clicked.connect(self.handleCreate)

        self.roomName = QLineEdit("Enter room name", self)
        self.roomName.setGeometry(100, 100, 400, 30)

        self.show()

    @pyqtSlot()
    def handleCreate(self):

        payload = {}
        payload["master"] = self.masterName
        payload["roomName"] = self.roomName.text()

        result = requests.post('http://' + self.serverIp + ':8080/room', json=payload)
        
        if(result.text == "Success"):
            self.gameRoom = GameRoom(self.roomName.text(), self.masterName, self.serverIp)
            self.gameRoom.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Error', result.text)




    
