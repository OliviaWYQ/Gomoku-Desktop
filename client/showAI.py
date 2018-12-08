#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 15:11:56 2018

@author: yiqianwang

AI
"""

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QMessageBox, QPushButton
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt
from chessboard import chessboard as CB
import random

class useAI(object):
    def __init__(self, board_size):
        self.board_size = board_size
        self.obj = CB(self.board_size)

    def getval(self, i, j):
        self.usr_x = i
        self.usr_y = j
        self.AI_x = random.randint(0, self.board_size-1)
        self.AI_y = random.randint(0, self.board_size-1)
        return self.AI_x, self.AI_y