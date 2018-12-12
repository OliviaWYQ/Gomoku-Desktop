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
import requests

from utils import pop_info_and_back

class rank(QWidget):
    def __init__(self, user_name, server_ip, auth_headers, manual_hook, login_hook):
        super(rank, self).__init__()
        self.user_name = user_name
        self.server_ip = server_ip
        self.auth_headers = auth_headers
        self.manual_hook = manual_hook
        self.login_hook = login_hook
        # self.setGeometry(330, 100, 280, 330)
        self.setWindowTitle("Gomoku Game Manual")
        self.setWindowIcon(QIcon('chessboard/gomoku_icon.png'))

        self.myrank()

        self.show()

        self.request()

    def request(self):
        response_top = requests.get('http://%s:8080/rank/all'\
            % self.server_ip,\
            headers=self.auth_headers)
        response_info = requests.get('http://%s:8080/rank/byusername/%s'\
            % (self.server_ip, self.user_name),\
            headers=self.auth_headers)
        try:
            top_three = response_top.json()
            my_info = response_info.json()
            # print(top_three)
            # print(my_info)
            # print(top_three[0])
            
            self.no1.setText("No.1: %s (%d)"\
                % (top_three[0]['userName'], top_three[0]['rankScore']))
            self.no2.setText("No.2: %s (%d)"\
                % (top_three[1]['userName'], top_three[1]['rankScore']))
            self.no3.setText("No.3: %s (%d)"\
                % (top_three[2]['userName'], top_three[2]['rankScore']))

            rank = requests.get('http://%s:8080/rank/byscore/%d'\
                % (self.server_ip, my_info['rankScore']),\
                headers=self.auth_headers)
            # print(rank)
            # print(rank.text)
            self.rank_label.setText("You're No.%s (%d)"\
                % (rank.text, my_info['rankScore']))
            self.win_rate_label.setText("Win rate: %3.2f%%"\
                % (my_info["winRate"]/100.0))
            self.show()
        except:
            pop_info_and_back(self, response_info.text, self.login_hook)

    def myrank(self):
        # top rank
        self.title = QLabel("Online Ranking", self)
        self.title.setFont(QFont('Arial', 20, QFont.Bold))
        self.title.move(80, 10)
        # no1
        self.no1 = QLabel('No.1:                                 ', self)
        self.no1.setFont(QFont('Arial', 16, QFont.Bold))
        self.no1.move(80, 60)
        # no2
        self.no2 = QLabel('No.2:                                 ', self)
        self.no2.setFont(QFont('Arial', 16, QFont.Bold))
        self.no2.move(80, 110)
        # no3
        self.no3 = QLabel('No.3:                                 ', self)
        self.no3.setFont(QFont('Arial', 16, QFont.Bold))
        self.no3.move(80, 160)
        # # id label
        # self.id_label = QLabel("Your id is " + self.user_name, self)
        # self.id_label.setFont(QFont('Arial', 16, QFont.Bold))
        # self.id_label.move(80, 210)
        # win rate
        self.win_rate_label = QLabel("Win rate:                 ", self)
        self.win_rate_label.setFont(QFont('Arial', 16, QFont.Bold))
        self.win_rate_label.move(80, 290)
        # rank label
        self.rank_label = QLabel("You're No.                   ", self)
        self.rank_label.setFont(QFont('Arial', 16, QFont.Bold))
        self.rank_label.move(80, 240)
        # back
        self.back_button = QPushButton("  Back  ", self)
        self.back_button.clicked.connect(self.back)
        self.back_button.move(190, 330)

    def back(self):
        self.manual_hook()
        self.close()

# def main():
#    app = QApplication(sys.argv)
#    exe = rank('12345', None)
#    exe.show()
#    sys.exit(app.exec_())

# if __name__ == '__main__':
#    main()