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
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QMessageBox, QPushButton
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt
from chessboard import chessboard as CB
#from showAI import ai
from ai import ai
import requests
#from login import *
#from choosechessboard import ChooseBtn
from music import musicplayer

class GomokuOffline(QWidget):
    def __init__(self, user_name, server_ip, my_chessboard_type, my_font, manual_hook, usecolor, opponent, difficulty):
        super().__init__()
        self.chessboard_type = my_chessboard_type
        self.username = user_name
        self.usecolor = usecolor
        self.opponent = opponent
        # init ai name
        self.difficulty = difficulty
        self.ai = ai(self.chessboard_type, self.difficulty, self.usecolor)
        if self.opponent == 1: # guest
            self.ifAI = 0
            if usecolor == 1:
                self.username_b = self.username
                self.username_w = "Guest"
            elif usecolor == 2:
                self.username_b = "Guest"
                self.username_w = self.username
        elif self.opponent == 2: # AI
            self.ifAI = 1
            if usecolor == 1:
                self.username_b = self.username
                self.username_w = "AlphaGomoku"
            elif usecolor == 2:
                self.username_b = "AlphaGomoku"
                self.username_w = self.username
        else:
            self.username_b = self.username_w = None
            print('opponent error')

        #init ai turn
        if self.ifAI:
            if self.usecolor == 1: # use black
                self.usrturn = 1
            elif self.usecolor == 2: # use white
                self.usrturn = 0
            else:
                self.usrturn = 0
                print('usecolor error')

        current_path = sys.path[0] + '/'
        print(current_path)
        self.manual_hook = manual_hook
        self.server_ip = server_ip

        self.my_font  = my_font
        self.chooseboard = QPixmap(current_path + 'chessboard/chessboard14.png')
        self.width_chessboard = 715
        self.height_chessboard = 689
        self.bgmusic = musicplayer()

        self.muted = False
        # 9*9
        if self.chessboard_type == 9:
            self.chooseboard = QPixmap(current_path + 'chessboard/chessboard8.png')
            self.width_chessboard = 443
            self.height_chessboard = 443
            self.margin = 28
            self.cbnum = 8
        # 15*15
        elif self.chessboard_type == 15:
            self.chooseboard = QPixmap(current_path + 'chessboard/chessboard14.png')
            self.width_chessboard = 715
            self.height_chessboard = 689
            self.margin = 20
            self.cbnum = 14
        else:
            print('error cbnum!')

        # other
        self.d_piece = 36
        self.r_piece = self.d_piece / 2
        self.grid_w = (self.width_chessboard - (self.margin * 2)) / self.cbnum
        self.grid_h = (self.height_chessboard - (self.margin * 2)) / self.cbnum
        self.restart()

    def restart(self):
        #CB init
        self.obj = CB(self.cbnum+1)
        self.obj.reset()
        self.winnervalue = 0
        self.setting()
        if self.chessboard_type == 9:
            self.showchessboard8()
        elif self.chessboard_type == 15:
            self.showchessboard14()
        else:
            print('error cbnum!')
        self.gamestart()
        self.setMouseTracking(True)

    def setting(self):
        # init user interface
        self.setGeometry(330, 70, self.width_chessboard + 200, self.height_chessboard) # set window size
        self.setWindowTitle("Gomoku Game") # set window title
        #self.setWindowIcon(QIcon('chessboard/gomoku_icon.png')) # set window icon
        self.black = QPixmap('chessboard/black.png') # set black piece
        self.white = QPixmap('chessboard/white.png') # set white piece
        self.many_black = QPixmap('chessboard/manyblack.png') # set many black
        self.many_white = QPixmap('chessboard/manywhite.png') # set many white
        self.setCursor(Qt.PointingHandCursor) # set mouse shape

    def showchessboard8(self):
        # show chessboard
        self.background = QLabel(self)
        self.background.setPixmap(self.chooseboard)
        self.background.setScaledContents(True)
        # show many black
        self.user_black = QLabel(self)
        self.user_black.setPixmap(self.many_black)
        self.user_black.move(450, 10)
        # show many white
        self.user_white = QLabel(self)
        self.user_white.setPixmap(self.many_white)
        self.user_white.move(450, self.height_chessboard - 195)

        # # show playername in black
        # self.player_b = QLabel(self)
        # self.player_b.setText("Black:    " + self.username_b)
        # self.player_b.move(475, 203)
        # self.player_b.setFont(QFont(self.my_font, 16, QFont.Bold))
        # # show playername in white
        # self.player_w = QLabel(self)
        # self.player_w.setText("White:    " + self.username_w)
        # self.player_w.move(475, self.height_chessboard - 213)
        # self.player_w.setFont(QFont(self.my_font, 16, QFont.Bold))

        self.id_label = QLabel("Id: " + self.username, self)
        self.id_label.move(475, 203)
        self.id_label.setFont(QFont(self.my_font, 16, QFont.Bold))

        self.turn_label = QLabel("Black side...", self)
        self.turn_label.move(475, self.height_chessboard - 213)
        self.turn_label.setFont(QFont(self.my_font, 16, QFont.Bold))

        self.back_button = QPushButton("  Back  ", self)
        self.back_button.clicked.connect(self.handle_back)
        self.back_button.move(560, 415)

        self.mute_button = QPushButton("Next", self)
        self.mute_button.clicked.connect(self.handle_next)
        self.mute_button.move(560, 355)
        self.mute_button.resize(self.back_button.sizeHint())

        self.mute_button = QPushButton("Mute", self)
        self.mute_button.clicked.connect(self.handle_mute)
        self.mute_button.move(560, 385)
        self.mute_button.resize(self.back_button.sizeHint())

    def showchessboard14(self):
        # show chessboard
        self.background = QLabel(self)
        self.background.setPixmap(self.chooseboard)
        self.background.setScaledContents(True)
        # show many black
        self.user_black = QLabel(self)
        self.user_black.setPixmap(self.many_black)
        self.user_black.move(720, 10)
        # show many white
        self.user_white = QLabel(self)
        self.user_white.setPixmap(self.many_white)
        self.user_white.move(720, self.height_chessboard - 195)
        # show playername in black
        self.player_b = QLabel(self)
        self.player_b.setText("Black: " + self.username_b)
        self.player_b.move(750, 220)
        self.player_b.setFont(QFont(self.my_font, 16, QFont.Bold))
        # show playername in white
        self.player_w = QLabel(self)
        self.player_w.setText("White: " + self.username_w)
        self.player_w.move(750, self.height_chessboard - 230)
        self.player_w.setFont(QFont(self.my_font, 16, QFont.Bold))

        self.id_label = QLabel("Id: " + self.username, self)
        self.id_label.move(750, 270)
        self.id_label.setFont(QFont(self.my_font, 16, QFont.Bold))

        self.turn_label = QLabel("Black side...", self)
        self.turn_label.move(750, 300)
        self.turn_label.setFont(QFont(self.my_font, 16, QFont.Bold))

        self.back_button = QPushButton("  Back  ", self)
        self.back_button.clicked.connect(self.handle_back)
        self.back_button.move(730, 375)

        self.mute_button = QPushButton("Next", self)
        self.mute_button.clicked.connect(self.handle_next)
        self.mute_button.move(820, 345)
        self.mute_button.resize(self.back_button.sizeHint())

        self.mute_button = QPushButton("Mute", self)
        self.mute_button.clicked.connect(self.handle_mute)
        self.mute_button.move(730, 345)
        self.mute_button.resize(self.back_button.sizeHint())

    def handle_back(self):
        self.manual_hook()
        self.bgmusic.stop()
        self.close()

    def handle_mute(self):
        if self.muted:
            self.bgmusic.unmute()
            self.mute_button.setText("Mute")
        else:
            self.bgmusic.mute()
            self.mute_button.setText("Unmute")
        self.muted = not self.muted

    def handle_next(self):
        if self.muted == False:
            self.bgmusic.nextsong()

    def addmusic(self):
        try:
            # background music
            self.bgmusic.start()
        except KeyboardInterrupt:
            self.bgmusic.stop()

    def gamestart(self):
        #game start
        #self.addmusic()
        #location of a piece
        self.piece = QLabel(self)
        self.piece.setMouseTracking(True)
        self.piece.pos = None
        # draw a piece, total 15 *15
        self.put = [QLabel(self) for i in range((self.cbnum+1) * (self.cbnum+1))]
        self.step = 1
        self.color = self.black # black first
        self.colornum = 1
    '''
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("press!")
        super().mousePressEvent(event)
    '''

    def mouseReleaseEvent(self, event):
        if self.ifAI:
            if self.usrturn:
                self.piece.pos = event.pos()
                if self.piece.pos:
                    self.i = round((self.piece.pos.x() - self.margin) / self.grid_w)
                    self.j = round((self.piece.pos.y() - self.margin) / self.grid_h)
                # check margin
                if (self.ai.changevalue(self.i, self.j, self.colornum) == 0):
                    print("Invalid! (step: %d, x: %d ,y: %d, color: %d)"  % (self.step, self.i, self.j, self.colornum))
                    self.i = None
                    self.j = None
                else:
                    print('step: %d, 网格坐标: ( x: %d ,y: %d, color: %d )' % (self.step, self.i, self.j, self.colornum))
                    #CB check winner value
                    self.winnervalue = self.ai.checkwinner()
                    print('winner:', self.winnervalue)
                    if self.winnervalue != 0:
                        self.paint(event)
                        self.showGameEnd(self.winnervalue)
                    else:
                        self.paint(event)
                        self.usrturn = not self.usrturn
                        self.nextstep()
                self.update()
            if not self.usrturn:
                if self.step == 1:
                    self.aix = self.chessboard_type // 2
                    self.aiy = self.chessboard_type // 2
                    print('ai first', self.aix, self.aix)
                    self.ai.changevalue(self.aix, self.aiy, self.colornum)
                    self.piece.pos = event.pos()
                else:
                    print('input: ( x: %d ,y: %d, color: %d )' % ( self.i, self.j, self.colornum))
                    self.aix, self.aiy = self.ai.decision(self.i, self.j)
                    print('step: %d, AI 网格坐标: ( x: %d ,y: %d, color: %d )' % (self.step, self.aix, self.aiy, self.colornum))
                self.i = self.aix
                self.j = self.aiy
                self.winnervalue = self.ai.checkwinner()
                print('winner:', self.winnervalue)
                if self.winnervalue != 0:
                    self.paint(event)
                    self.showGameEnd(self.winnervalue)
                else:
                    self.paint(event)
                    self.usrturn = not self.usrturn
                    self.nextstep()
                self.update()
        else:
            self.piece.pos = event.pos()
            if self.piece.pos:
                self.i = round((self.piece.pos.x() - self.margin) / self.grid_w)
                self.j = round((self.piece.pos.y() - self.margin) / self.grid_h)
            #print('test: step: %d, 网格坐标: ( x: %d ,y: %d, color: %d )' % (self.step, self.i, self.j, self.colornum))
            #CB input winner value
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
                x = self.margin + self.i * self.grid_w - self.r_piece
                y = self.margin + self.j * self.grid_h - self.r_piece
                self.put[self.step].setGeometry(x, y, self.d_piece, self.d_piece) # draw piece to grid

    def nextstep(self):
        # next step
        self.step += 1
        # change color
        if self.color == self.black:
            self.color = self.white
            self.colornum = 2
            self.turn_label.setText("White side...")
        else:
            self.color = self.black
            self.colornum = 1
            self.turn_label.setText("Black side...")

    def showGameEnd(self, winner):
        self.sendMatch(winner, self.obj.sendsteps())
        if winner == 1:
            winnername = "Black"
        elif winner == 2:
            winnername = "White"
        else:
            winnername = "TIE GAME! None of You"
        self.label = QLabel("About Qt MessageBox")
        button = QMessageBox.question(self,"Gomoku Game Information",
                                      self.tr("Game End\n%s Wins!\nQuit or Start A New Game?" % winnername),
                                      QMessageBox.Retry|QMessageBox.Close,
                                      QMessageBox.Retry)
        if button == QMessageBox.Retry:
            self.label.setText("Question button/Retry")
            self.cam = GomokuOffline(self.username, self.server_ip, self.chessboard_type, self.my_font, self.manual_hook, self.usecolor, self.opponent,self.difficulty)
            self.cam.show()
            self.close()

        elif button == QMessageBox.Close:
            self.label.setText("Question button/Close")
            self.bgmusic.stop()
            self.manual_hook()
            self.close()
            #raise SystemExit(0)
        else:
            return

    def sendMatch(self, winFlag, moves):
        payload = {}
        payload["user1id"] = self.username_b
        payload["user2id"] = self.username_w
        payload["user1win"] = winFlag
        payload["moves"] = moves
        #payload = {'user':'user', 'pass':'123456'}
        _ = requests.post('http://' + self.server_ip + ':8080/match', json=payload)
        # print(payload)
        # if (r.text == "Success"):
        #     QMessageBox.warning(self, 'Success', 'Success')
        #     self.game = Gomoku(self.user_name.text())
        #     self.game.show()
        #     self.close()
        # else:
        #     QMessageBox.warning(self, 'Error', 'Bad user or password')

def main():
    app = QApplication(sys.argv)
    mygame = GomokuOffline("12345", "52.207.232.53", 9, 'Roman times', None, 2, 2)
    mygame.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
