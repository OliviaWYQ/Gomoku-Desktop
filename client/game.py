from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

D_PIECE = 36
R_PIECE = D_PIECE / 2
WIDTH_CHESSBOARD = 715
HEIGHT_CHESSBOARD = 689
MARGIN = 20
GRID_W = (WIDTH_CHESSBOARD - (MARGIN * 2)) / 14
GRID_H = (HEIGHT_CHESSBOARD - (MARGIN* 2)) / 14

class Gomoku(QWidget):
    # main gaming UI

    end_game_signal = pyqtSignal(int)

    def __init__(self, is_master, room_name,\
                master_name, guest_name,\
                master_stone, server_ip,\
                web_socket, back_hook,\
                watch_game=False):
        super().__init__()

        self.end_game_signal.connect(self.show_game_end)

        self.watch_game = watch_game

        self.step_no = 0
        self.oth_step = 0
        self.is_master = is_master

        if self.is_master:
            self.user_name = master_name
        else:
            self.user_name = guest_name

        self.room_name = room_name

        # if self.watch_game:
        #     uri = 'ws://' + server_ip + ':8080/playing'

        #     headers = [("role", 'a'),
        #         ("roomName", room_name),
        #         ("userName", web_socket),
        #         ("masterStone", 1)]
        # else:
        self.web_socket = web_socket

        self.back_hook = back_hook
        self.server_ip = server_ip

        if master_stone == 1:
            self.username_b = master_name
            self.username_w = guest_name
            self.put_stone = self.is_master
        else:
            self.username_w = master_name
            self.username_b = guest_name
            self.put_stone = not self.is_master

        if self.put_stone:
            self.my_stone = 1
        else:
            self.my_stone = 2

        #self.web_socket = SocketCli(uri, headers=headers)

        self.reset_socket_hook()

        self.restart()

    def restart(self):
        #CB init
        # self.obj = CB()
        # self.obj.reset()
        self.winnervalue = 0
        self.show_chess_board()

        self.game_start()
        self.setMouseTracking(True)

    def show_chess_board(self):
        # init user interface
        self.setGeometry(330, 70, WIDTH_CHESSBOARD + 200, HEIGHT_CHESSBOARD) # set window size
        self.setWindowTitle("Gomoku Game") # set window title
        self.setWindowIcon(QIcon('chessboard/gomoku_icon.png')) # set window icon
        self.chessboard14 = QPixmap('chessboard/chessboard14.png') # set background
        self.black = QPixmap('chessboard/black.png') # set black piece
        self.white = QPixmap('chessboard/white.png') # set white piece
        self.many_black = QPixmap('chessboard/manyblack.png') # set many black
        self.many_white = QPixmap('chessboard/manywhite.png') # set many white
        self.setCursor(Qt.PointingHandCursor) # set mouse shape
        # show chessboard
        background = QLabel(self)
        background.setPixmap(self.chessboard14)
        background.setScaledContents(True)
        # show many black
        user_black = QLabel(self)
        user_black.setPixmap(self.many_black)
        user_black.move(720, 10)
        # show many white
        user_white = QLabel(self)
        user_white.setPixmap(self.many_white)
        user_white.move(720, HEIGHT_CHESSBOARD - 195)
        # show playername in black
        player_black = QLabel(self)
        player_black.setText("Black:    " + self.username_b)
        player_black.move(750, 220)
        player_black.setFont(QFont("Roman times", 16, QFont.Bold))
        # show playername in white
        player_white = QLabel(self)
        player_white.setText("White:    " + self.username_w)
        player_white.move(750, HEIGHT_CHESSBOARD - 230)
        player_white.setFont(QFont("Roman times", 16, QFont.Bold))

    def game_start(self):
        #game start
        #location of a piece
        self.piece = QLabel(self)
        self.piece.setMouseTracking(True)
        self.piece.pos = None
        # draw a piece, total 15 *15
        self.put = [QLabel(self) for i in range(15 * 15)]
        # self.step = 1
        if self.put_stone:
            self.color = self.black
        else:
            self.color = self.white

        if self.watch_game:
            self.web_socket.connect()
        # self.colornum = 1

    def mouseReleaseEvent(self, event):
        if self.put_stone:
            #self.put_stone = False

            self.piece.pos = event.pos()
            if self.piece.pos:

                self.i = round((self.piece.pos.x() - MARGIN) / GRID_W)
                self.j = round((self.piece.pos.y() - MARGIN) / GRID_H)

                if self.i < 15 and self.j < 15 and\
                    self.i >= 0 and self.j >= 0:
                    to_send = self.encode(self.i, self.j)

                    self.web_socket.send(to_send)

    def encode(self, x, y):
        message = x
        message |= (y << 4)
        message |= (self.my_stone << 8)
        message |= (self.step_no << 10)
        return str(message)

    def paint(self, i, j, color):
        self.put[self.step_no + self.oth_step].setPixmap(color)
        x = MARGIN + i * GRID_W - R_PIECE
        y = MARGIN + j * GRID_H - R_PIECE
        # draw piece to grid
        self.put[self.step_no + self.oth_step].setGeometry(x, y, D_PIECE, D_PIECE)

        if self.watch_game:
            self.step_no += 1

    def put_a_stone(self, pos_by_int):
        x = pos_by_int & 0b1111
        y = (pos_by_int >> 4) & 0b1111
        player = (pos_by_int >> 8) & 0b11
        step = (pos_by_int >> 10) & 0b1111_1111
        win_flag = (pos_by_int >> 18) & 0b111

        print('step: %d, x: %d ,y: %d, p: %d, win_flag: %d' % (step, x, y, player, win_flag))

        if player == 1:
            self.paint(x, y, self.black)
        else:
            self.paint(x, y, self.white)
        if not self.watch_game:
            if self.my_stone == player:
                self.step_no = step + 1
                self.put_stone = False
            else:
                self.oth_step = step + 1
                self.put_stone = True
        if win_flag == 0:
            pass
        elif win_flag == 1:
            print("black win")
            self.end_game_signal.emit(1)
        elif win_flag == 2:
            print("white win")
            self.end_game_signal.emit(2)
        elif win_flag == 3:
            print("LOL")
            self.end_game_signal.emit(3)

        self.update()

    @pyqtSlot(int)
    def show_game_end(self, winner):
        if self.watch_game:
            if winner == 3:
                info = "Draw. lol"
            elif winner == 1:
                info = "Black win!"
            elif winner == 2:
                info = "White win!"
            elif winner == 6:
                info = "Someone quitted."
            button = QMessageBox.question(self, "Info",\
                                      info,\
                                      QMessageBox.Ok,\
                                      QMessageBox.Ok)
            if button == QMessageBox.Ok:
                self.back_hook()
                self.close()
            else:
                self.close()
                raise SystemExit(0)
            return

        if winner == 3:
            info = "Draw. lol"
        else:
            if winner == 6:
                info = "Your opponent quitted."
            elif winner == self.my_stone:
                info = "You win! Nice!"
            else:
                info = "You lose."
        button = QMessageBox.question(self, "Info",\
                                      info,\
                                      QMessageBox.Ok,\
                                      QMessageBox.Ok)
        if button == QMessageBox.Ok:
            self.back_hook()
            self.close()
        else:
            self.close()
            raise SystemExit(0)

    def reset_socket_hook(self):
        self.web_socket.hook(self)

    def handle_message(self, message):
        print("Received: ", message)
        if message[0] == 'J':
            # join signal
            print("Should not receive join signal: ", message)
        else:
            try:
                signal = int(message)
                if signal < 0:
                    # START_SIGNAL = -1
                    # GUEST_READY_SIGNAL = -2
                    # GUEST_UNREADY_SIGNAL = -3
                    # GUEST_LEAVE_SIGNAL = -4
                    # MASTER_DELETE_SIGNAL = -5
                    # END_SIGNAL = -6

                    if signal == -6:
                        self.end_game_signal.emit(6)
                    else:
                        print("Should not receive other control signals: ", signal)
                else:
                    # moving signal
                    self.put_a_stone(signal)
            except:
                print("Unvalid message format.")
