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
        self.setGeometry(330, 100, 420, 150)
        self.setWindowTitle("Choose opponent")
        self.setWindowIcon(QIcon('chessboard/gomoku_icon.png'))
        self.user_name = user_name
        self.usecolor = 1
        self.opponent = 1
        self.difficulty = 1
        self.choose_opponent()

    def renew(self):
        self.usecolor = 1
        self.opponent = 1
        self.choose_opponent()

    def choose_opponent(self):
        self.choosecolor = QLabel("Choose color:", self)
        self.choosecolor.move(30, 25)

        self.colors = QComboBox(self)
        self.colors.addItems(["Black", "White"])
        self.colors.setGeometry(180, 25, 100, 20)
        self.colors.currentIndexChanged.connect(self.handle_color_change)

        self.choosecolor = QLabel("Choose opponent:", self)
        self.choosecolor.move(30, 65)

        self.colors = QComboBox(self)
        self.colors.addItems(["Guest", "AI"])
        self.colors.setGeometry(180, 65, 100, 20)
        self.colors.currentIndexChanged.connect(self.handle_opponent_change)

        self.choosediff = QLabel("Choose AI Difficulty:", self)
        self.choosediff.move(30, 105)

        self.diff = QComboBox(self)
        self.diff.addItems(["Easy", "Medium", "Hard"])
        self.diff.setGeometry(180, 105, 100, 20)
        self.diff.currentIndexChanged.connect(self.handle_difficulty)
        self.diff.setEnabled(False)

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.handle_back)
        self.back_button.move(300, 60)

        self.confirm_button = QPushButton("Confirm", self)
        self.confirm_button.clicked.connect(self.opponent_confirm)
        self.confirm_button.move(300, 100)

        self.confirm_button.resize(self.confirm_button.sizeHint())
        self.back_button.resize(self.confirm_button.sizeHint())

    def handle_difficulty(self):
        if self.diff.currentText() == "Easy":
            self.difficulty = 1
        elif self.diff.currentText() == "Medium":
            self.difficulty = 2
        else:
            self.difficulty = 3

    def handle_color_change(self):
        if self.colors.currentText() == "Black":
            self.usecolor = 1
        else:
            self.usecolor = 2

    def handle_opponent_change(self):
        if self.colors.currentText() == "Guest":
            self.opponent = 1
        else:
            self.diff.setEnabled(True)
            self.opponent = 2

    def opponent_confirm(self):
        print("color", self.usecolor)
        print("opponent", self.opponent)
        print("difficulty", self.difficulty)
        self.mygame = GomokuOffline(self.user_name, self.server_ip, self.chooseboard, \
                                    self.myfont, self.manual_hook, self.usecolor, self.opponent, self.difficulty)
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