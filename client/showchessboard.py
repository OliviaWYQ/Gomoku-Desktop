from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
import requests
#from login import *
from choosechessboard import ChooseBtn

# main gaming UI
class Gomoku(QWidget):
    def __init__(self, userName, serverIp, mycbtype, myfonttype):
        super().__init__()
        self.start_game_signal.connect(self.showGameEnd)
        self.step_no = 0
        self.oth_step = 0
        self.isMaster = isMaster

        if self.isMaster:
            self.userName = masterName
        else:
            self.userName = guestName

        self.roomName = roomName
        self.ws = websocket
        self.backHook = backHook
        self.serverIp = serverIp
        self.username_b = userName
        self.username_w = "Guest"
        self.cbty = mycbtype
        self.myfont  = myfonttype
        self.chooseboard = QPixmap('chessboard/chessboard14.png')
        self.width_chessboard = 715
        self.height_chessboard = 689
        self.bgmusic = musicplayer()

        # 9*9
        if self.cbty == 9:
            self.chooseboard = QPixmap('chessboard/chessboard8.png')
            self.width_chessboard = 443
            self.height_chessboard = 443
            self.margin = 28
            self.cbnum = 8
        # 15*15
        elif self.cbty == 15:
            self.chooseboard = QPixmap('chessboard/chessboard14.png')
            self.width_chessboard = 715
            self.height_chessboard = 689
            self.margin = 20
            self.cbnum = 14
        else:
            print('error cbnum!')

        # other
        self.D_piece = 36
        self.R_piece = self.D_piece / 2
        self.grid_w = (self.width_chessboard - (self.margin * 2)) / self.cbnum
        self.grid_h = (self.height_chessboard - (self.margin * 2)) / self.cbnum
        self.restart()

    def restart(self):    
        #CB init
        self.obj = CB(self.cbnum+1)
        self.obj.reset()
        self.winnervalue = 0
        self.Setting()
        if self.cbty == 9:
            self.showchessboard8()
        elif self.cbty == 15:
            self.showchessboard14()
        else:
            print('error cbnum!')
        self.gamestart()
        self.setMouseTracking(True)

    def Setting(self):
        # init user interface
        self.setGeometry(330, 70, self.width_chessboard + 200, self.height_chessboard) # set window size
        self.setWindowTitle("Gomoku Game") # set window title
        self.setWindowIcon(QIcon('chessboard/gomoku_icon.png')) # set window icon
        self.black = QPixmap('chessboard/black.png') # set black piece
        self.white = QPixmap('chessboard/white.png') # set white piece
        self.manyblack = QPixmap('chessboard/manyblack.png') # set many black
        self.manywhite = QPixmap('chessboard/manywhite.png') # set many white
        self.setCursor(Qt.PointingHandCursor) # set mouse shape

    def showchessboard8(self):
        # show chessboard
        background = QLabel(self)
        background.setPixmap(self.chooseboard)
        background.setScaledContents(True)
        # show many black
        user_black = QLabel(self)
        user_black.setPixmap(self.manyblack)
        user_black.move(450, 10)
        # show many white
        user_white = QLabel(self)
        user_white.setPixmap(self.manywhite)
        user_white.move(450, self.height_chessboard - 195)
        # show playername in black
        Player_b = QLabel(self)
        Player_b.setText("Black:    " + self.username_b)
        Player_b.move(475, 203)
        Player_b.setFont(QFont(self.myfont, 16, QFont.Bold))
        # show playername in white
        Player_w = QLabel(self)
        Player_w.setText("White:    " + self.username_w)
        Player_w.move(475, self.height_chessboard - 213)
        Player_w.setFont(QFont(self.myfont, 16, QFont.Bold))

    def showchessboard14(self):
        # show chessboard
        background = QLabel(self)
        background.setPixmap(self.chooseboard)
        background.setScaledContents(True)
        # show many black
        user_black = QLabel(self)
        user_black.setPixmap(self.manyblack)
        user_black.move(720, 10)
        # show many white
        user_white = QLabel(self)
        user_white.setPixmap(self.manywhite)
        user_white.move(720, self.height_chessboard - 195)
        # show playername in black
        Player_b = QLabel(self)
        Player_b.setText("Black:    " + self.username_b)
        Player_b.move(750, 220)
        Player_b.setFont(QFont(self.myfont, 16, QFont.Bold))
        # show playername in white
        Player_w = QLabel(self)
        Player_w.setText("White:    " + self.username_w)
        Player_w.move(750, self.height_chessboard - 230)
        Player_w.setFont(QFont(self.myfont, 16, QFont.Bold))

    def addmusic(self):
        try:
            # background music
            self.bgmusic.start()
        except KeyboardInterrupt:
            self.bgmusic.stop()

    def gamestart(self):
        #game start
        #location of a piece
        self.piece = QLabel(self)
        self.piece.setMouseTracking(True)
        self.piece.pos = None
        # draw a piece, total 15 *15
        self.put = [QLabel(self) for i in range(self.cbnum+1 * self.cbnum+1)]
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
            self.i = round((self.piece.pos.x() - self.margin) / self.grid_w)
            self.j = round((self.piece.pos.y() - self.margin) / self.grid_h)
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
                x = self.margin + self.i * self.grid_w - self.R_piece
                y = self.margin + self.j * self.grid_h - self.R_piece
                self.put[self.step].setGeometry(x, y, self.D_piece, self.D_piece) # draw piece to grid

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

    def showGameEnd(self, winner):
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
            self.cam = Gomoku(self.username_b, self.serverIp, self.cbty, self.myfont)
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
    mygame = Gomoku("12345", "54.173.206.13", 9, 'Roman times')
    mygame.show()
    mygame.addmusic()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
'''
