import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from room import *
import requests

class GameHall(QWidget):
    def __init__(self, userName, serverIp):
        super().__init__()
        self.serverIp = serverIp
        self.userName = userName

        self.title = "Game Hall"
        self.top = 100
        self.left = 100
        self.width = 600
        self.height = 500

        self.refresh()

        self.browse(0)
        #self.InitUI()

    def refresh(self):
        self.roomList = requests.get('http://' + self.serverIp + ':8080/room/all').json()
        self.currentPage = 0
        self.maxPage = int(len(self.roomList) / 10)

    def browse(self, page):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        createButton = QPushButton('create', self)
        createButton.move(100, 450)
        createButton.clicked.connect(self.handleCreate)

        joinButton = QPushButton('join', self)
        joinButton.move(200, 450)
        joinButton.clicked.connect(self.handleCreate)

        watchButton = QPushButton('watch', self)
        watchButton.move(300, 450)
        watchButton.clicked.connect(self.handleCreate)

        # self.userName = QLineEdit("12345", self)
        # self.userName.setGeometry(100, 100, 400, 30)
    
        # self.pwd = QLineEdit("123", self)
        # self.pwd.setEchoMode(QLineEdit.Password)
        # self.pwd.setGeometry(100, 200, 400, 30)
        # self.pwd.setEchoMode(QLineEdit.Password)

        # self.serverIp = QLineEdit("54.173.206.13", self)
        # self.serverIp.setGeometry(100, 400, 400, 30)

        self.show()

    @pyqtSlot()
    def handleCreate(self):
        self.createRoom = CreateRoom(self.userName, self.serverIp)
        self.createRoom.show()
        self.close()




    
