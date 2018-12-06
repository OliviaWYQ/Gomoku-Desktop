#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 09:09:49 2018

@author: yiqianwang
main manual
"""

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QMessageBox, QPushButton
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt
#from showchessboard import Gomoku
from showchessboardOffline import GomokuOffline
from choosechessboard import ChooseBtn
#from variable import setvar
from hall import GameHallWindow

class manual(QWidget):
    def __init__(self, user_name, server_ip, auth_headers, login_hook):
        super(manual, self).__init__()

        self.auth_headers = auth_headers
        self.login_hook = login_hook

        self.setGeometry(330, 100, 360, 450)
        self.setWindowTitle("Gomoku Game Manual")
        self.setWindowIcon(QIcon('chessboard/gomoku_icon.png'))
        self.server_ip = server_ip
        self.user_name = user_name
        self.myset = ChooseBtn(self.manual_hook)
        self.showmanual()

    def showmanual(self, base_x=120, base_y=80, offset_x=0, offset_y=70):

        # id label
        self.id_label = QLabel("Your id: " + self.user_name, self)
        self.id_label.move(30, 30)

        # Setting
        self.offline_setting_button = QPushButton("Offline Setting",self)
        self.offline_setting_button.clicked.connect(self.handle_offline_setting)
        self.offline_setting_button.move(base_x, base_y)

        # Offline Game
        self.offline_game_button = QPushButton("Offline Game",self)
        self.offline_game_button.clicked.connect(self.handle_offline_game)
        self.offline_game_button.move(base_x, base_y+offset_y)

        # Online Game
        self.online_game_button = QPushButton("Online Game",self)
        self.online_game_button.clicked.connect(self.handle_online_game)
        self.online_game_button.move(base_x, base_y+2*offset_y)

        # Ranking
        self.ranking_button = QPushButton("Ranking",self)
        self.ranking_button.clicked.connect(self.handle_ranking)
        self.ranking_button.move(base_x, base_y+3*offset_y)

        # Ranking
        self.logout_button = QPushButton("Log out",self)
        self.logout_button.clicked.connect(self.handle_logout)
        self.logout_button.move(base_x, base_y+4*offset_y)

        # set button size
        self.offline_setting_button.resize(self.offline_game_button.sizeHint())
        # self.offline_game_button.resize(self.offline_game_button.sizeHint())
        self.online_game_button.resize(self.offline_game_button.sizeHint())
        self.ranking_button.resize(self.offline_game_button.sizeHint())
        self.logout_button.resize(self.offline_game_button.sizeHint())


    def handle_logout(self):
        self.login_hook()
        self.close()

    def handle_offline_setting(self):
        #print("handle_offline_setting")
        self.myset.show()
        self.close()

    def handle_offline_game(self):
        if self.myset.var.OK == 0:
            QMessageBox.warning(self, 'Setting Error', 'Confirm the setting first')
        else:
            self.update()
            print("board:", "\nftype:", self.myset.var.fonttype, "\ncbtyp3:", self.myset.var.cbtype, "\nOK:", self.myset.var.OK)
            self.chooseboard = self.myset.var.cbtype
            self.myfont = self.myset.var.fonttype
            self.mygame = GomokuOffline(self.user_name, self.server_ip, self.chooseboard, self.myfont, self.manual_hook)
            self.mygame.show()
            # do not use addmusic(), will block the program !!
            # self.mygame.addmusic() # do not use addmusic(), will block the program !!
            self.close()

    def handle_online_game(self):
        print("handle_online_game")
        self.hall = GameHallWindow(self.user_name, self.server_ip, self.auth_headers, self.login_hook, self.manual_hook)
        self.hall.show()
        self.close()

    def handle_ranking(self):
        print("handle_ranking")

    def manual_hook(self):
        self.show()

def main():
   app = QApplication(sys.argv)
   exe = manual("12345", "52.207.232.53", None, None)
   exe.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()