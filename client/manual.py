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
from showchessboard import Gomoku
from choosechessboard import ChooseBtn
#from variable import setvar

class manual(QWidget):
    def __init__(self, userName, serverIp):
        super(manual, self).__init__()
        self.setGeometry(330, 100, 380, 450)
        self.setWindowTitle("Gomoku Game Manual")
        self.setWindowIcon(QIcon('chessboard/gomoku_icon.png'))
        self.serverIp = serverIp
        self.username_b = userName
        self.myset = ChooseBtn()
        self.showmanual()

    def showmanual(self):
        # Offline Game
        self.btn1 = QPushButton("Offline Game",self)
        self.btn1.clicked.connect(self.Action1)
        self.btn1.resize(self.btn1.sizeHint())
        self.btn1.move(120, 150)

        # Online Game
        self.btn2 = QPushButton("Online Game",self)
        self.btn2.clicked.connect(self.Action2)
        self.btn2.resize(self.btn1.sizeHint())
        self.btn2.move(120, 250)

        # Setting
        self.btn0 = QPushButton("Setting",self)
        self.btn0.clicked.connect(self.Action0)
        self.btn0.resize(self.btn1.sizeHint())
        self.btn0.move(120, 50)

        # Ranking
        self.btn3 = QPushButton("Ranking",self)
        self.btn3.clicked.connect(self.Action3)
        self.btn3.resize(self.btn1.sizeHint())
        self.btn3.move(120, 350)

    def Action0(self):
        print("Action0")
        self.myset.show()

    def Action1(self):
        if self.myset.var.OK == 0:
            QMessageBox.warning(self, 'Setting Error', 'Confirm the setting first')
        else:
            print("board:", "\nftype:", self.myset.var.fonttype, "\ncbtyp3:", self.myset.var.cbtype, "\nOK:", self.myset.var.OK)
            self.chooseboard = self.myset.var.cbtype
            self.myfont = self.myset.var.fonttype
            self.mygame = Gomoku(self.username_b, self.serverIp, self.chooseboard, self.myfont)
            self.mygame.show()

    def Action2(self):
        print("Action2")

    def Action3(self):
        print("Action3")

def main():
   app = QApplication(sys.argv)
   exe = manual("12345", "54.173.206.13")
   exe.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()