#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 13:45:19 2018

@author: yiqianwang

Main function
"""

from showchessboard3 import *
from login import *
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt
from chessboard import chessboard as CB

def main():
    app = QApplication(sys.argv)

    root = Tk()
    lf = LoginFrame(root)
    root.mainloop()

    # game = Gomoku()
    # game.show()
    # sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
