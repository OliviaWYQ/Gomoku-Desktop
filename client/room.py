#import sys
# from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton,\
    QMessageBox, QComboBox, QLineEdit, QLabel
from PyQt5.QtGui import QIcon
import requests
from ws4py.client.threadedclient import WebSocketClient

from game import Gomoku
from utils import pop_info_and_back

START_SIGNAL = -1
GUEST_READY_SIGNAL = -2
GUEST_UNREADY_SIGNAL = -3
GUEST_LEAVE_SIGNAL = -4
MASTER_DELETE_SIGNAL = -5
END_SIGNAL = -6
BLACK_STONE_SIGNAL = -7
WHITE_STONE_SIGNAL = -8

START_SIGNAL_MESSAGE = '-1'
GUEST_READY_SIGNAL_MESSAGE = '-2'
GUEST_UNREADY_SIGNAL_MESSAGE = '-3'
GUEST_LEAVE_SIGNAL_MESSAGE = '-4'
MASTER_DELETE_SIGNAL_MESSAGE = '-5'
END_SIGNAL_MESSAGE = '-6'
BLACK_STONE_SIGNAL_MESSAGE = '-7'
WHITE_STONE_SIGNAL_MESSAGE = '-8'

class SocketCli(WebSocketClient):
    def hook(self, to_influence):
        self.to_influence = to_influence

    def opened(self):
        #self.send("open")
        pass

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, message):
        self.to_influence.handle_message(message.data.decode("utf-8"))

class GameRoomWindow(QWidget):

    start_game_signal = pyqtSignal()

    def __init__(self, room_name, master_name, guest_name,\
        server_ip, is_master, hall_hook, login_hook, auth_headers):
        super().__init__()

        self.auth_headers = auth_headers

        self.start_game_signal.connect(self.start_game)

        self.hall_hook = hall_hook
        self.login_hook = login_hook

        self.layout = QHBoxLayout()
        self.room_name = room_name
        self.server_ip = server_ip
        #self.user_name = user_name
        self.is_master = is_master
        self.master_stone = 1

        self.master_name = master_name
        self.guest_name = guest_name

        self.title = "Game Hall"
        self.top = 100
        self.left = 100
        self.width = 600
        self.height = 200

        self.ready = False

        self.init_socket()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setWindowIcon(QIcon('chessboard/gomoku_icon.png')) # set window icon
        self.stone_color_label = QLabel("Creator will use:", self)
        self.stone_color_label.move(255, 14)

        self.colors = QComboBox(self)
        self.colors.addItems(["Black", "White"])
        self.colors.setGeometry(250, 40, 100, 20)
        self.colors.setEnabled(self.is_master)
        if self.is_master:
            self.colors.currentIndexChanged.connect(self.handle_color_change)

        self.start_button_label = QLabel("Start the game:", self)
        self.start_button_label.move(405, 14)

        self.start_button = QPushButton('Start', self)
        self.start_button.move(400, 34)
        self.start_button.clicked.connect(self.handle_start)
        self.start_button.setEnabled(False)

        self.leave_button_label = QLabel("Leave the game:", self)
        self.leave_button_label.move(255, 74)

        self.leave_button = QPushButton('  Leave  ', self)
        self.leave_button.move(250, 94)
        self.leave_button.clicked.connect(self.handle_leave)

        self.guest_status_label = QLabel("Guest is:", self)
        self.guest_status_label.move(405, 74)

        self.ready_button = QPushButton('Unready', self)
        self.ready_button.move(400, 94)
        self.ready_button.clicked.connect(self.handle_ready)
        self.ready_button.setEnabled(not self.is_master)

        self.start_button.resize(self.leave_button.sizeHint())
        self.ready_button.resize(self.leave_button.sizeHint())

        self.room_status_label = QLabel(self)
        self.room_status_label.move(255, 140)

        # id label
        self.id_label = QLabel(self)
        self.id_label.move(40, 14)

        self.role_label = QLabel(self)
        self.role_label.move(40, 44)

        if self.is_master:
            self.id_label.setText("Your id: " + self.master_name)
            self.role_label.setText("You're creator of this room.")
            self.room_status_label.setText("Waiting for player ...")
        else:
            self.id_label.setText("Your id: " + self.guest_name)
            self.role_label.setText("You're guest of this room.")
            self.room_status_label.setText("Creator id: " + self.master_name)

        self.show()

    def handle_message(self, message):
        print("Received: ", message)
        if message[0] == 'J':
            # join signal
            if self.is_master:
                self.guest_name = message[1:]
                self.room_status_label.setText("Guest id: " + self.guest_name)
                if self.colors.currentText() == 'Black':
                    self.master_stone = 1
                    self.web_socket.send(BLACK_STONE_SIGNAL_MESSAGE)
                else:
                    self.master_stone = 2
                    self.web_socket.send(WHITE_STONE_SIGNAL_MESSAGE)
        else:
            try:
                signal = int(message)
                print("signal", signal)
                if signal < 0:
                    # START_SIGNAL = -1
                    # GUEST_READY_SIGNAL = -2
                    # GUEST_UNREADY_SIGNAL = -3
                    # GUEST_LEAVE_SIGNAL = -4
                    # MASTER_DELETE_SIGNAL = -5
                    # END_SIGNAL = -6

                    if self.is_master:
                        if signal == GUEST_READY_SIGNAL:
                            print("ready")
                            self.ready = True
                            self.start_button.setEnabled(True)
                            self.ready_button.setText("Ready")
                        elif signal == GUEST_UNREADY_SIGNAL:
                            print("unready")
                            self.ready = False
                            self.start_button.setEnabled(False)
                            self.ready_button.setText("Unready")
                        elif signal == GUEST_LEAVE_SIGNAL:
                            self.ready = False
                            self.start_button.setEnabled(self.ready)
                            self.ready_button.setText("Unready")
                            self.guest_name = None
                            self.room_status_label.setText("Waiting for player ...")
                        elif signal == START_SIGNAL:
                            print("try to start")
                            self.start_game_signal.emit()
                        else:
                            print("Unvalid master control signal.")
                    else:
                        if signal == START_SIGNAL:
                            print("try to start")
                            self.start_game_signal.emit()
                        elif signal == MASTER_DELETE_SIGNAL:
                            self.hall_hook()
                            self.close()
                            # TODO: pop a message box
                        elif signal == BLACK_STONE_SIGNAL:
                            self.master_stone = 1
                            self.colors.setCurrentIndex(self.colors.findText('Black'))
                        elif signal == WHITE_STONE_SIGNAL:
                            self.master_stone = 2
                            self.colors.setCurrentIndex(self.colors.findText('White'))
                        else:
                            print("Unvalid guest control signal.")
                    # control signal
                else:
                    # should not be processed now
                    print("Moving signal, game does not start yet.")
            except:
                print("Unvalid message format.")

    @pyqtSlot()
    def start_game(self):
        # return to hall after the match
        # if return to room, must init socket, reset the to_influence by calling hook()
        #hall_hook = self.hall_hook

        self.game_board = Gomoku(self.is_master, self.room_name,\
                                self.master_name, self.guest_name,\
                                self.master_stone, self.server_ip,\
                                self.web_socket, self.hall_hook)
        self.game_board.show()
        self.close()

    def init_socket(self):
        # uri = 'ws://' + self.server_ip + ':8080/playing'
        # role can be: "m" for master, "g" for guest, "a" for audience
        # if master use balck stone, "master_stone:1", if white, "master_stone:2"

        # if self.colors.currentText() == 'Black':
        #     master_stone = '1'
        # else:
        #     master_stone = '2'

        self.uri = 'ws://' + self.server_ip + ':8080/playing'
        # self.uri = 'ws://' + self.server_ip + ':8080/test'

        if self.is_master:
            role = 'm'
            user_name = self.master_name
        else:
            role = 'g'
            user_name = self.guest_name

        self.headers = [("role", role),\
            ("roomName", self.room_name),\
            ("userName", user_name),\
            ("masterStone", self.master_stone)]
        self.web_socket = SocketCli(self.uri, headers=self.headers)
        self.web_socket.connect()
        self.web_socket.hook(self)

        if not self.is_master:
            print("before send join")
            self.web_socket.send('J'+self.guest_name)
            print("sent join")

    @pyqtSlot()
    def handle_color_change(self):
        if self.colors.currentText() == 'Black':
            self.master_stone = 1
            print("send: change to balck")
            self.web_socket.send(BLACK_STONE_SIGNAL_MESSAGE)
        else:
            self.master_stone = 2
            print("send: change to white")
            self.web_socket.send(WHITE_STONE_SIGNAL_MESSAGE)


    @pyqtSlot()
    def handle_start(self):
        # donot need to send info to redis,
        # done by server

        self.web_socket.send(START_SIGNAL_MESSAGE)


    @pyqtSlot()
    def handle_leave(self):
        # donot need to send info to redis,
        # done by server

        if self.is_master:
            response = requests.get('http://' + self.server_ip +\
                ':8080/room/delete/'+ self.room_name + '/' +\
                self.master_name, headers=self.auth_headers)
            # if response.text == 'Success':
            #     self.web_socket.send(MASTER_DELETE_SIGNAL_MESSAGE)
            #     self.hall_hook()
            #     self.close()
            # elif response.text == "Unauthorized or timeout.":
            #     pop_info_and_back(self, response.text, self.login_hook)
            # else:
            print('#### Info: master delete: ' + response.text)
            if response.text == 'Success':
                print("Success")
                self.web_socket.send(MASTER_DELETE_SIGNAL_MESSAGE)
                self.web_socket.close()
                self.hall_hook()
            else:
                print("Fail")
                self.web_socket.close()
                self.hall_hook(refresh=True)
            self.close()
        else:
            response = requests.get('http://' + self.server_ip +\
                ':8080/room/leave/'+ self.room_name + '/' +\
                self.guest_name, headers=self.auth_headers)
            # if response.text == 'Success':
            #     self.web_socket.send(GUEST_LEAVE_SIGNAL_MESSAGE)
            #     self.hall_hook()
            #     self.close()
            # elif response.text == "Unauthorized or timeout.":
            #     pop_info_and_back(self, response.text, self.login_hook)
            # else:
            #     print(response.text)
            print('#### Info: guest leave: ' + response.text)
            self.web_socket.send(GUEST_LEAVE_SIGNAL_MESSAGE)
            self.web_socket.close()
            self.hall_hook()
            self.close()
            if response.text == 'Success':
                print("Success")
                self.web_socket.close()
                self.hall_hook()
            else:
                print("Fail")
                self.web_socket.close()
                self.hall_hook(refresh=True)
            self.close()

    @pyqtSlot()
    def handle_ready(self):
        # donot need to send info to redis,
        # done by server

        if self.ready:
            self.ready = False
            self.web_socket.send(GUEST_UNREADY_SIGNAL_MESSAGE)
            self.ready_button.setText("Unready")
        else:
            self.ready = True
            self.web_socket.send(GUEST_READY_SIGNAL_MESSAGE)
            self.ready_button.setText("Ready")



########################### Create Room  ##############################

class CreateRoomWindow(QWidget):
    def __init__(self, master_name, server_ip, auth_headers, hall_hook, login_hook):
        super().__init__()

        self.auth_headers = auth_headers

        self.hall_hook = hall_hook
        self.login_hook = login_hook

        self.server_ip = server_ip
        self.master_name = master_name

        self.title = "Create a room"
        self.top = 100
        self.left = 100
        self.width = 600
        self.height = 300

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.create_button = QPushButton('Create', self)
        self.create_button.move(100, 180)
        self.create_button.clicked.connect(self.handle_create)

        self.create_button = QPushButton('Back', self)
        self.create_button.move(200, 180)
        self.create_button.clicked.connect(self.handle_back)

        self.room_name_label = QLabel("Room name:", self)
        self.room_name_label.setGeometry(100, 70, 400, 30)

        self.room_name = QLineEdit(self)
        self.room_name.setGeometry(100, 100, 400, 30)

        self.show()

    @pyqtSlot()
    def handle_back(self):
        self.hall_hook()
        self.close()

    @pyqtSlot()
    def handle_create(self):
        payload = {}
        payload["master"] = self.master_name
        payload["roomName"] = self.room_name.text().strip()
        
        if len(payload["roomName"]) == 0:
            _ = QMessageBox.question(self, 'Info',\
                'Enter a room name.\n (leading and ending spaces will be removed)',\
                QMessageBox.Ok, QMessageBox.Ok)
            return

        response = requests.post('http://' + self.server_ip + ':8080/room',\
            json=payload, headers=self.auth_headers)

        if response.text == "Success":
            self.game_room = GameRoomWindow(self.room_name.text(),\
                self.master_name, None, self.server_ip,\
                True, self.hall_hook, self.login_hook,\
                self.auth_headers)
            self.game_room.show()
            self.close()
        elif response.text == "Unauthorized or timeout.":
            pop_info_and_back(self, response.text, self.login_hook)
        else:
            QMessageBox.warning(self, 'Error', response.text)
