#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 10:40:38 2018

@author: yiqianwang

Gomoku Game
First Iteration
chessboard UI
"""

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt
from chessboard import chessboard as CB
import requests
#from login import *

D_piece = 36
R_piece = D_piece / 2
width_chessboard = 715
height_chessboard = 689
margin = 20
grid_w = (width_chessboard - (margin * 2)) / 14
grid_h = (height_chessboard - (margin* 2)) / 14


class Gomoku(QWidget):
    def __init__(self, userName, serverIp):
        super().__init__()
        #username_b = userName
        self.serverIp = serverIp
        self.username_b = userName
        self.username_w = "Guest"
        self.restart()
        
    def restart(self):    
        #CB init
        self.obj = CB()
        self.obj.reset()
        self.winnervalue = 0
        self.showchessboard()
        #login
        '''
        root = Tk()
        lf = LoginFrame(root)
        root.mainloop()
        '''
        self.gamestart()
        self.setMouseTracking(True)
    
    def showchessboard(self):
        # init user interface
        self.setGeometry(330, 70, width_chessboard + 200, height_chessboard) # set window size
        self.setWindowTitle("Gomoku Game") # set window title
        self.setWindowIcon(QIcon('chessboard/gomoku_icon.png')) # set window icon
        self.chessboard14 = QPixmap('chessboard/chessboard14.png') # set background
        self.black = QPixmap('chessboard/black.png') # set black piece
        self.white = QPixmap('chessboard/white.png') # set white piece
        self.manyblack = QPixmap('chessboard/manyblack.png') # set many black
        self.manywhite = QPixmap('chessboard/manywhite.png') # set many white
        self.setCursor(Qt.PointingHandCursor) # set mouse shape
        # show chessboard
        background = QLabel(self)
        background.setPixmap(self.chessboard14)
        background.setScaledContents(True)
        # show many black
        user_black = QLabel(self)
        user_black.setPixmap(self.manyblack)
        user_black.move(720, 10)
        # show many white
        user_white = QLabel(self)
        user_white.setPixmap(self.manywhite)
        user_white.move(720, height_chessboard - 195)
        # show playername in black
        Player_b = QLabel(self)
        Player_b.setText("Black:    " + self.username_b)
        Player_b.move(750, 220)
        Player_b.setFont(QFont("Roman times", 16, QFont.Bold))
        # show playername in white
        Player_w = QLabel(self)
        Player_w.setText("White:    " + self.username_w)
        Player_w.move(750, height_chessboard - 230)
        Player_w.setFont(QFont("Roman times", 16, QFont.Bold))
        
    def gamestart(self):
     
        
        #game start
        #location of a piece
        self.piece = QLabel(self)
        self.piece.setMouseTracking(True)
        self.piece.pos = None
        # draw a piece, total 15 *15
        self.put = [QLabel(self) for i in range(15 * 15)]
        self.step = 1
        self.color = self.black # change to black first
        self.colornum = 1
        
    '''
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("press!")
        super().mousePressEvent(event)
    '''
    
    def mouseReleaseEvent(self, event):   
        self.piece.pos = event.pos()
        if self.piece.pos:
            self.i = round((self.piece.pos.x() - margin) / grid_w)
            self.j = round((self.piece.pos.y() - margin) / grid_h)
        #print('test: step: %d, 网格坐标: ( x: %d ,y: %d, color: %d )' % (self.step, self.i, self.j, self.colornum))
        
        #CB input value
        if (self.obj.changevalue(self.i, self.j, self.colornum) == 0):
            print("Invalid! (step: %d, x: %d ,y: %d, color: %d)"  % (self.step, self.i, self.j, self.colornum))
            self.i = None
            self.j = None
            
        else:
            print('step: %d, 网格坐标: ( x: %d ,y: %d, color: %d )' % (self.step, self.i, self.j, self.colornum))
            #CB check value
            self.winnervalue = self.obj.checkwinner()
            print('winner:', self.winnervalue)
            if self.winnervalue != 0:
                self.paint(event)
                self.showGameEnd(self.winnervalue)
            else:
                self.paint(event)
                self.nextstep()
        self.update()
        
    def paint(self, event):
        if self.piece.pos:
            self.put[self.step].setPixmap(self.color)
            if self.i != None and self.j != None:
                x = margin + self.i * grid_w - R_piece
                y = margin + self.j * grid_h - R_piece
                self.put[self.step].setGeometry(x, y, D_piece, D_piece) # draw piece to grid
                
    def nextstep(self):
        # next step
        self.step += 1
        # change color
        if self.color == self.black:
            self.color = self.white
            self.colornum = 2
        else:
            self.color = self.black
            self.colornum = 1
                
    def showGameEnd(self, winner, ):
        self.sendMatch(winner, self.obj.sendsteps())
        if winner == 1:
            winnername = self.username_b
        elif winner == 2:
            winnername = self.username_w
        else:
            winnername = "TIE GAME! None of You"
        self.label = QLabel("About Qt MessageBox")  
        button = QMessageBox.question(self,"Gomoku Game Information",  
                                      self.tr("Game End\n%s Win!\nQuit or Start A New Game?" % winnername),  
                                      QMessageBox.Retry|QMessageBox.Close,  
                                      QMessageBox.Retry)  
        if button == QMessageBox.Retry:  
            self.label.setText("Question button/Retry")
            self.cam = Gomoku(self.username_b, self.serverIp)
            self.cam.show()
            self.close()
            
        elif button == QMessageBox.Close:  
            self.label.setText("Question button/Close")  
            raise SystemExit(0)
        else:  
            return


    def sendMatch(self, winFlag, moves):
        
        payload = {}
        payload["user1id"] = self.username_b
        payload["user2id"] = self.username_w
        payload["user1win"] = winFlag
        payload["moves"] = moves
        #payload = {'user':'user', 'pass':'123456'}
        r = requests.post('http://' + self.serverIp + ':8080/match', json=payload)
        
        # print(payload)

        # if (r.text == "Success"):
        #     QMessageBox.warning(self, 'Success', 'Success')
        #     self.game = Gomoku(self.userName.text())
        #     self.game.show()
        #     self.close()
        # else:
        #     QMessageBox.warning(self, 'Error', 'Bad user or password')

'''    
def main():
    app = QApplication(sys.argv)
    game = Gomoku()
    game.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
'''