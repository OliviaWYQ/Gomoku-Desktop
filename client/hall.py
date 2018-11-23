import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from room import GameRoomWindow, CreateRoomWindow
import requests

class GameHallWindow(QWidget):
    def __init__(self, userName, serverIp):
        super().__init__()
        self.serverIp = serverIp
        self.userName = userName

        self.currentPage = -1;

        self.title = "Game Hall"
        self.top = 100
        self.left = 100
        self.width = 700
        self.height = 500

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.createButton = QPushButton('Create', self)
        self.createButton.move(580, 20)
        self.createButton.clicked.connect(self.handleCreate)

        self.actionButton = QPushButton('Action', self)
        self.actionButton.move(580, 70)
        self.actionButton.clicked.connect(self.handleAction)

        self.refreshButton = QPushButton('Refresh', self)
        self.refreshButton.move(580, 120)
        self.refreshButton.clicked.connect(self.refresh)

        self.exitButton = QPushButton('Exit', self)
        self.exitButton.move(580, 390)
        self.exitButton.clicked.connect(self.handleExit)

        self.roomsObserved = QTableWidget(self)
        self.roomsObserved.setRowCount(10)
        self.roomsObserved.setColumnCount(2)

        self.roomsObserved.setHorizontalHeaderLabels(['Room Name','Status'])
        self.roomsObserved.setGeometry(50, 20, 500, 400)

        # cannot edit
        self.roomsObserved.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # choose whole row
        self.roomsObserved.setSelectionBehavior(QAbstractItemView.SelectRows)
        # at most select one row
        self.roomsObserved.setSelectionMode(QAbstractItemView.SingleSelection)
        # hide vertical header
        self.roomsObserved.verticalHeader().setVisible(False)

        self.roomsObserved.setColumnWidth(0, 400)
        self.roomsObserved.setColumnWidth(1, 99)
        self.roomsObserved.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.roomsObserved.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.roomsObserved.setCornerButtonEnabled(False)
        self.roomsObserved.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.refresh()

        self.browse(0)

        self.show()

    @pyqtSlot()
    def refresh(self):
        self.roomList = requests.get('http://' + self.serverIp + ':8080/room/all').json()

        print(self.roomList)
        
        self.currentPage = 0
        self.maxPage = int(len(self.roomList) / 10)
        self.currentPage = -1
        self.browse(0)

    def browse(self, page):
        if(self.currentPage != page):
            self.currentPage = page
            for i in range(10):
                if(self.currentPage*10+i >= len(self.roomList)):
                    break
                self.addLine(self.roomList[self.currentPage*10 + i], i)

    def addLine(self, aRoom, rowNum):
        self.roomsObserved.setItem(rowNum, 0, QTableWidgetItem(aRoom['roomName']))
        self.roomsObserved.setItem(rowNum, 1, QTableWidgetItem(aRoom['roomStatus']))


    @pyqtSlot()
    def handleCreate(self):
        self.createRoomPage = CreateRoomWindow(self.userName, self.serverIp)
        self.createRoomPage.show()
        self.close()

    @pyqtSlot()
    def handleAction(self):
        pass

    @pyqtSlot()
    def handleExit(self):
        self.close()
