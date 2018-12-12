#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 15:27:11 2018

@author: yiqianwang
"""

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QMessageBox, QPushButton, QComboBox
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt
from showchessboardOffline import GomokuOffline

class chooseAI(QWidget):
    def __init__(self, user_name, server_ip, chooseboard, myfont, manual_hook):
        super(chooseAI, self).__init__()
        self.manual_hook = manual_hook
        self.server_ip = server_ip
        self.chooseboard = chooseboard
        self.myfont = myfont
        self.setGeometry(330, 100, 400, 100)
        self.setWindowTitle("Choose opponent")
        self.setWindowIcon(QIcon('chessboard/gomoku_icon.png'))
        self.user_name = user_name
        self.usecolor = 1
        self.opponent = 1
        self.choose_opponent()

    def renew(self):
        self.usecolor = 1
        self.opponent = 1
        self.choose_opponent()

    def choose_opponent(self):
        self.choosecolor = QLabel("Choose color:", self)
        self.choosecolor.move(30, 20)

        self.colors = QComboBox(self)
        self.colors.addItems(["Black", "White"])
        self.colors.setGeometry(30, 50, 100, 20)
        self.colors.currentIndexChanged.connect(self.handle_color_change)

        self.choosecolor = QLabel("Choose opponent:", self)
        self.choosecolor.move(150, 20)

        self.colors = QComboBox(self)
        self.colors.addItems(["Guest", "AI"])
        self.colors.setGeometry(150, 50, 100, 20)
        self.colors.currentIndexChanged.connect(self.handle_opponent_change)

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.handle_back)
        self.back_button.move(280, 20)

        self.confirm_button = QPushButton("Confirm", self)
        self.confirm_button.clicked.connect(self.opponent_confirm)
        self.confirm_button.move(280, 50)

        self.confirm_button.resize(self.confirm_button.sizeHint())
        self.back_button.resize(self.confirm_button.sizeHint())

    def handle_color_change(self):
        if self.colors.currentText() == "Black":
            self.usecolor = 1
        else:
            self.usecolor = 2

    def handle_opponent_change(self):
        if self.colors.currentText() == "Guest":
            self.opponent = 1
        else:
            self.opponent = 2

    def opponent_confirm(self):
        print("color", self.usecolor)
        print("opponent", self.opponent)
        self.mygame = GomokuOffline(self.user_name, self.server_ip, self.chooseboard, \
                                    self.myfont, self.manual_hook, self.usecolor, self.opponent)
        self.mygame.show()
        self.close()

    def handle_back(self):
        self.manual_hook()
        self.close()

def main():
   app = QApplication(sys.argv)
   exe = chooseAI("12345", "52.207.232.53", 9, 'Roman times', None)
   exe.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()