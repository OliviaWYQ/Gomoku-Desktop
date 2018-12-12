"""
Game hall window, could be entered from:
login window (main.py);
game room window (room.py);
create room window (room.py)
"""

#import sys
#from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QPushButton,\
    QMessageBox, QTableWidget, QAbstractItemView,\
    QTableWidgetItem, QHeaderView, QApplication
from PyQt5.QtGui import QIcon
import requests
import sys

from room import GameRoomWindow, CreateRoomWindow, SocketCli
from game import Gomoku
from utils import pop_info_and_back

class GameHallWindow(QWidget):
    """Game hall window, create/ join/ watch a match"""

    def __init__(self, username, server_ip, auth_headers, login_hook, manual_hook):
        super().__init__()
        self.auth_headers = auth_headers
        self.login_hook = login_hook
        self.manual_hook = manual_hook

        self.server_ip = server_ip
        self.username = username

        self.current_page = -1

        self.title = "Game Hall"
        self.top = 100
        self.left = 100
        self.width = 700
        self.height = 500

        self.init_ui()

        self.refresh()

    def init_ui(self):
        """
        init the ui of game hall:
        table, buttons.
        And set the style of them
        """
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('chessboard/gomoku_icon.png')) # set window icon
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.create_room_button = QPushButton('Create', self)
        self.create_room_button.move(580, 20)
        self.create_room_button.clicked.connect(self.handle_create_room)

        self.action_button = QPushButton('Action', self)
        self.action_button.move(580, 70)
        self.action_button.clicked.connect(self.handle_action)
        # disable the action button at first
        self.action_button.setEnabled(False)

        self.refresh_button = QPushButton('Refresh', self)
        self.refresh_button.move(580, 120)
        self.refresh_button.clicked.connect(self.refresh)

        self.back_button = QPushButton('Back', self)
        self.back_button.move(580, 340)
        self.back_button.clicked.connect(self.handle_back)

        self.exit_button = QPushButton('Exit', self)
        self.exit_button.move(580, 390)
        self.exit_button.clicked.connect(self.handle_exit)

        # room list, using table
        self.rooms_observed = QTableWidget(self)
        self.rooms_observed.setRowCount(10)
        self.rooms_observed.setColumnCount(2)
        # change the action button after selecting a room
        self.rooms_observed.clicked.connect(self.handle_click_room_observed)
        # set column name
        self.rooms_observed.setHorizontalHeaderLabels(['Room Name', 'Status'])
        self.rooms_observed.setGeometry(50, 20, 500, 400)

        # cannot edit
        self.rooms_observed.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # choose whole row
        self.rooms_observed.setSelectionBehavior(QAbstractItemView.SelectRows)
        # at most select one row
        self.rooms_observed.setSelectionMode(QAbstractItemView.SingleSelection)
        # hide vertical header
        self.rooms_observed.verticalHeader().setVisible(False)
        # fix the table width
        self.rooms_observed.setColumnWidth(0, 400)
        self.rooms_observed.setColumnWidth(1, 99)
        # disable the scrol bar
        self.rooms_observed.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.rooms_observed.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # disable resizing table
        self.rooms_observed.setCornerButtonEnabled(False)
        self.rooms_observed.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.create_room_button.resize(self.refresh_button.sizeHint())
        self.action_button.resize(self.refresh_button.sizeHint())
        self.exit_button.resize(self.refresh_button.sizeHint())
        self.back_button.resize(self.refresh_button.sizeHint())

        self.show()

    @pyqtSlot()
    def refresh(self):
        """handle clicking refresh button, refresh the room info in the table"""
        response = requests.get('http://%s:8080/room/all'\
            % self.server_ip,\
            headers=self.auth_headers)
        try:
            self.room_list = response.json()
            print(self.room_list)

            self.max_page = int(len(self.room_list) / 10)
            self.current_page = -1
            self.browse(0)

            # refresh chane the room list, should init the action btn
            self.action_button.setEnabled(False)
            self.action_button.setText("Action")
        except:
            pop_info_and_back(self, response.text, self.login_hook)

            # info = response.text
            # button = QMessageBox.question(self, "Info",\
            #                           info,\
            #                           QMessageBox.Ok,\
            #                           QMessageBox.Ok)
            # if button == QMessageBox.Ok:
            #     self.login_hook()
            #     self.close()
            # else:
            #     self.close()
            #     raise SystemExit(0)

    def browse(self, page):
        """choose the page of rooms to browse"""
        if self.current_page != page:
            self.rooms_observed.clearContents()
            self.current_page = page
            for i in range(10):
                if self.current_page*10+i >= len(self.room_list):
                    break
                self.add_line(self.room_list[self.current_page*10 + i], i)

    def add_line(self, a_room, row_num):
        """add a room into the table, call by browse"""
        self.rooms_observed.setItem(row_num, 0, QTableWidgetItem(a_room['roomName']))
        self.rooms_observed.setItem(row_num, 1, QTableWidgetItem(a_room['roomStatus']))

    @pyqtSlot()
    def handle_create_room(self):
        """create a room, call create window"""
        self.create_room_page = CreateRoomWindow(master_name=self.username,\
            server_ip=self.server_ip,\
            hall_hook=self.hall_hook,\
            login_hook=self.login_hook,\
            auth_headers=self.auth_headers)

        self.create_room_page.show()
        self.close()

    @pyqtSlot()
    def handle_action(self):
        """watch or join or disable based on the room chosen"""
        # selected_row = self.rooms_observed.currentRow()
        action = self.action_button.text()
        print(action)
        if action == "Join":
            self.join_room()
        elif action == "Watch":
            # try to watch the game
            self.watch_game()

    def watch_game(self):
        """call by action_btn, watch a match in certain room"""
        selected_row = self.rooms_observed.currentRow()
        master_name = self.room_list[selected_row + self.current_page * 10]["master"]
        guest_name = self.room_list[selected_row + self.current_page * 10]["guest"]
        room_name = self.rooms_observed.item(selected_row, 0).text()

        uri = 'ws://' + self.server_ip + ':8080/playing'

        socket_headers = [("role", 'a'),\
            ("roomName", room_name),\
            ("userName", self.username),\
            ("masterStone", 1)]

        self.web_socket = SocketCli(uri, headers=socket_headers)
        # self.web_socket.hook(self)

        self.game_board = Gomoku(True, room_name, master_name,\
            guest_name, 1, self.server_ip, self.web_socket,\
            self.hall_hook, True)
        self.game_board.show()
        self.close()

    @pyqtSlot()
    def handle_exit(self):
        """exit the programm, pop a window to ensure"""
        reply = QMessageBox.question(self, 'Exit', 'You sure to exit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # TODO: other actions
            self.close()

    @pyqtSlot()
    def handle_back(self):
        self.manual_hook()
        self.close()

    @pyqtSlot()
    def handle_click_room_observed(self):
        """
        select a room in the table,
        change the action_btn based on the game status
        """
        selected_row = self.rooms_observed.currentRow()
        try:
            select_status = self.rooms_observed.item(selected_row, 1).text()
            self.action_button.setEnabled(True)
            if select_status == 'Open':
                self.action_button.setText("Join")
            elif select_status == 'Playing':
                self.action_button.setText("Watch")
            else:
                self.action_button.setEnabled(False)
                self.action_button.setText("Action")
        except:
            self.action_button.setEnabled(False)
            self.action_button.setText("Action")

    def join_room(self):
        """join the room as a guest"""
        selected_row = self.rooms_observed.currentRow()
        try:
            room_name = self.rooms_observed.item(selected_row, 0).text()

            uri = "http://%s:8080/room/join/%s/%s"\
                % (self.server_ip, room_name, self.username)

            result = requests.get(uri, headers=self.auth_headers)

            print('from server: '+ result.text)

            if result.text == "Success":
                master_name = self.room_list[selected_row + self.current_page * 10]["master"]
                self.game_room = GameRoomWindow(room_name, master_name,\
                    self.username, self.server_ip, False, self.hall_hook,\
                    self.login_hook, self.auth_headers)
                self.game_room.show()
                self.close()
            else:
                QMessageBox.warning(self, 'Error', result.text)
        except Exception as e:
            print(e)
            QMessageBox.warning(self, 'Error', "Try again.")

    def hall_hook(self, refresh=True):
        self.show()
        if refresh:
            self.refresh()
            # self.browse(0)

def test():
    app = QApplication(sys.argv)
    exe = GameHallWindow("12345", "52.207.232.53", None, None, None)
    exe.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   test()