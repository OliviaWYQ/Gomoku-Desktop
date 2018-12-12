#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 14:06:52 2018

@author: yiqianwang

game help
"""
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QMessageBox, QPushButton
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt

class helper(QWidget):
    def __init__(self, manual_hook):
        super(helper, self).__init__()
        self.manual_hook = manual_hook
        self.setGeometry(330, 100, 600, 300)
        self.setWindowTitle("Gomoku Game Help")
        self.setWindowIcon(QIcon('chessboard/gomoku_icon.png'))
        self.notice()

    def notice(self):
        # text
        self.text = QLabel("Welcome to Gomoku Game", self)
        self.text.setFont(QFont('Arial', 20, QFont.Bold))
        self.text.move(100, 30)
        # text
        self.text = QLabel("You can play Gomoku Game both online and offline\n\n"+
                           "Choose a chessboard size before the offline game\n\n"+
                           "Change music by Next, Pause the music by Mute\n\n"+
                           "Enter the room number and wait till another player join you", self)
        self.text.setFont(QFont('Arial', 16, QFont.Bold))
        self.text.move(50, 80)
        # back
        self.back_button = QPushButton("  Back  ", self)
        self.back_button.clicked.connect(self.back)
        self.back_button.move(500, 230)

    def back(self):
        self.manual_hook()
        self.close()
'''
def main():
   app = QApplication(sys.argv)
   exe = helper(None)
   exe.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
'''