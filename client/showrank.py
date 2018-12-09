#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 18:45:34 2018

@author: yiqianwang

showrank
"""

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QMessageBox, QPushButton
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt

class rank(QWidget):
    def __init__(self, user_name, manual_hook):
        super(rank, self).__init__()
        self.user_name = user_name
        self.manual_hook = manual_hook
        self.setGeometry(330, 100, 280, 330)
        self.setWindowTitle("Gomoku Game Manual")
        self.setWindowIcon(QIcon('chessboard/gomoku_icon.png'))
        self.request()
        self.myrank()

    def request(self):
        self.no1 = 'None'
        self.no2 = 'None'
        self.no3 = 'None'
        self.user_rank = '0'

    def myrank(self):
        # top rank
        self.title = QLabel("Top Ranking", self)
        self.title.setFont(QFont('Arial', 20, QFont.Bold))
        self.title.move(80, 10)
        # no1
        self.No1 = QLabel("No. 1:    " + self.no1, self)
        self.No1.setFont(QFont('Arial', 16, QFont.Bold))
        self.No1.move(80, 60)
        # no2
        self.No2 = QLabel("No. 2:    " + self.no2, self)
        self.No2.setFont(QFont('Arial', 16, QFont.Bold))
        self.No2.move(80, 110)
        # no3
        self.No3 = QLabel("No. 3:    " + self.no3, self)
        self.No3.setFont(QFont('Arial', 16, QFont.Bold))
        self.No3.move(80, 160)
        # id label
        self.id_label = QLabel("Your id is " + self.user_name, self)
        self.id_label.setFont(QFont('Arial', 16, QFont.Bold))
        self.id_label.move(80, 210)
        # rank label
        self.rank_label = QLabel("Your ranking is " + self.user_rank, self)
        self.rank_label.setFont(QFont('Arial', 16, QFont.Bold))
        self.rank_label.move(80, 260)
        # back
        self.back_button = QPushButton("  Back  ", self)
        self.back_button.clicked.connect(self.back)
        self.back_button.move(190, 290)

    def back(self):
        self.manual_hook()
        self.close()

def main():
   app = QApplication(sys.argv)
   exe = rank('12345', None)
   exe.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()