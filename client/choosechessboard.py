#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 8 10:35:51 2018

@author: yiqianwang

smallchessboard
"""

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel, QGroupBox, QVBoxLayout, QMessageBox, QCheckBox, QHBoxLayout, QRadioButton, QGridLayout
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt
from variable import setvar

class ChooseBtn(QWidget):
    def __init__(self, parent = None):
        super(ChooseBtn, self).__init__(parent)
        self.setGeometry(330, 100, 600, 400)
        self.setWindowTitle("Setting")
        self.setWindowIcon(QIcon('chessboard/gomoku_icon.png'))
        # init
        # static val
        self.var = setvar()
        self.var.setvalue('cb8', 'chessboard/cb8.png')
        self.var.setvalue('cb14', 'chessboard/cb14.png')
        #self.var.setvalue('chessboard14', 'chessboard/chessboard14.png') # set background
        #self.var.setvalue('chessboard8', 'chessboard/chessboard8.png')
        self.var.setvalue('ftype1', 'Roman times')
        self.var.setvalue('ftype2', 'Arial')
        self.var.setvalue('ftype3', 'Mono')
        # variable
        self.var.cbtype = 15
        self.var.fonttype = 'ftype1'
        # set background
        self.cb14 = QPixmap(self.var.getvalue('cb14'))
        self.cb8 = QPixmap(self.var.getvalue('cb8'))
        self.type1 = self.var.getvalue('ftype1')
        self.type2 = self.var.getvalue('ftype2')
        self.type3 = self.var.getvalue('ftype3')
        self.Myfont = 'ftype1'
        self.chooseboard = 'cb14'
        #self.Myfont = self.var.getvalue(self.fonttype)
        #self.chooseboard = self.var.getvalue(self.cbtype)
        self.showsetting()

    def showsetting(self):
        # text
        choosetext = QLabel(self)
        choosetext.setText("Costomize Your Chessboard Size And Username Font Type")
        choosetext.setFont(QFont("Roman times", 16, QFont.Bold))

        # img
        cb8 = QLabel(self)
        cb8.setPixmap(self.cb8)
        cb14 = QLabel(self)
        cb14.setPixmap(self.cb14)
        self.bt1 = QPushButton("Confirm",self)
        self.bt1.clicked.connect(self.Action)
        self.bt1.resize(self.bt1.sizeHint())
        self.bt1.move(505, 3)

        # put text
        self.GroupBox0 = QGroupBox()
        layout0 = QHBoxLayout()
        self.GroupBox0.setLayout(layout0)
        layout0.addWidget(choosetext)

        # put img
        self.GroupBox1 = QGroupBox()
        layout1 = QGridLayout()
        self.GroupBox1.setLayout(layout1)
        layout1.addWidget(cb8, 1, 0)
        layout1.addWidget(cb14, 1, 1)

        # button1 for 9*9
        self.b1 = QRadioButton("9*9 chessboard")
        self.b1.setFont(QFont("Roman times", 16, QFont.Bold))
        self.b1.toggled.connect(lambda:self.btnstate(self.b1))
        # button2 for 15*15
        self.b2 = QRadioButton("15*15 chessboard")
        self.b2.setFont(QFont("Roman times", 16, QFont.Bold))
        self.b2.setChecked(True)
        self.b2.toggled.connect(lambda:self.btnstate(self.b2))

        # put button
        self.GroupBox2 = QGroupBox()
        layout2 = QHBoxLayout()
        self.GroupBox2.setLayout(layout2)
        layout2.addWidget(self.b1)
        layout2.addWidget(self.b2)

        # button3 for Roman Times
        self.b3 = QRadioButton(self.type1)
        self.b3.setChecked(True)
        self.b3.toggled.connect(lambda:self.btnstate(self.b3))
        self.b3.setFont(QFont(self.type1, 16, QFont.Bold))
        # button4 for Arial
        self.b4 = QRadioButton(self.type2)
        self.b4.toggled.connect(lambda:self.btnstate(self.b4))
        self.b4.setFont(QFont(self.type2, 16, QFont.Bold))
        # button5 for Helvetica
        self.b5 = QRadioButton(self.type3)
        self.b5.toggled.connect(lambda:self.btnstate(self.b5))
        self.b5.setFont(QFont(self.type3, 16, QFont.Bold))

        # put button
        self.GroupBox3 = QGroupBox()
        layout3 = QHBoxLayout()
        self.GroupBox3.setLayout(layout3)
        layout3.addWidget(self.b3)
        layout3.addWidget(self.b4)
        layout3.addWidget(self.b5)
        # show together
        mainLayout = QVBoxLayout()
        #mainLayout.addWidget(self.bt1)
        mainLayout.addWidget(self.GroupBox0)
        mainLayout.addWidget(self.GroupBox1)
        mainLayout.addWidget(self.GroupBox2)
        mainLayout.addWidget(self.GroupBox3)
        self.setLayout(mainLayout)

    def btnstate(self, b):
        if b.text() == "9*9 chessboard":
            if b.isChecked() == True:
                self.chooseboard = 'cb8'
                self.var.cbtype = 9
                print (b.text()+" is selected", self.var.cbtype)
        if b.text() == "15*15 chessboard":
            if b.isChecked() == True:
                self.chooseboard = 'cb14'
                self.var.cbtype = 15
                print (b.text()+" is selected", self.var.cbtype)
        if b.text() == self.type1:
            if b.isChecked() == True:
                self.Myfont = 'ftype1'
                print ("Font style is "+b.text())
        if b.text() == self.type2:
            if b.isChecked() == True:
                self.Myfont = 'ftype2'
                print ("Font style is "+b.text())
        if b.text() == self.type3:
            if b.isChecked() == True:
                self.Myfont = 'ftype3'
                print ("Font style is "+b.text())

    def Action(self):
        if self.bt1.isEnabled():
            #self.game = Gomoku("12345", "54.173.206.13")
            self.update()
            self.var.fonttype = self.var.getvalue(self.Myfont)
            #if self.chooseboard == 'cb14' or 'cb8':
            #    print('setting finish')
            #else:
            #    print('setting error!')
            #self.game.show()
            self.var.OK = 1
            #print("setting:", "\nftype:", self.var.fonttype, "\ncbtyp3:", self.chooseboard, self.var.cbtype, "\nOK:", self.var.OK)
            self.close()
            #raise SystemExit(0)

'''
def main():
   app = QApplication(sys.argv)
   ex = ChooseBtn()
   ex.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
'''