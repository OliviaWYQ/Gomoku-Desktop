"""
Entrance of the project, login& signup window
"""

import sys
#from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QMessageBox, QApplication, QLabel
from PyQt5.QtGui import QIcon
import requests
from manual import *
from hall import GameHallWindow

# IP = "localhost"
IP = "52.207.232.53"

class Window(QMainWindow):
    """Log in window"""

    def __init__(self, server_ip=IP):
        super().__init__()
        self.title = "Gomoku"
        self.top = 330
        self.left = 100
        self.width = 600
        self.height = 500

        self.server_ip = server_ip

        self.init_ui()

    def init_ui(self):
        """init the window, adding buttons and inputs"""
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setWindowIcon(QIcon('chessboard/gomoku_icon.png')) # set window icon

        self.user_name_label = QLabel("User name:", self)
        self.user_name_label.setGeometry(100, 70, 400, 30)

        self.user_name_input = QLineEdit("12345", self)
        self.user_name_input.setGeometry(100, 100, 400, 30)

        self.pwd_label = QLabel("Password:", self)
        self.pwd_label.setGeometry(100, 170, 400, 30)

        self.pwd_input = QLineEdit("123", self)
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.pwd_input.setGeometry(100, 200, 400, 30)
        self.pwd_input.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton('log in', self)
        login_btn.move(100, 300)
        login_btn.clicked.connect(self.handle_login)

        signup_btn = QPushButton('sign up', self)
        signup_btn.move(400, 300)
        signup_btn.clicked.connect(self.handle_signup)

        # self.server_ip = QLineEdit(IP, self)
        # self.server_ip.setGeometry(100, 400, 400, 30)

        self.show()

    @pyqtSlot()
    def handle_login(self):
        """handle clicking login button"""
        payload = {}
        payload["userName"] = self.user_name_input.text()
        payload["pass"] = self.pwd_input.text()
        #payload = {'user':'user', 'pass':'123456'}
        res = requests.post('http://' + self.server_ip + ':8080/auth/login', json=payload)
        print(res.text)

        print(payload["userName"])

        if len(res.text)>7 and res.text[:7] == "Success":
            # user_tooken = res[6:]
            # QMessageBox.warning(self, 'Success', 'Success')
            user_name = self.user_name_input.text()
            auth_headers = {'TOKEN': res.text[8:], 'USER_NAME': user_name}
            print(auth_headers)
            self.manual_window = manual(self.user_name_input.text(), self.server_ip, auth_headers, self.login_hook)
            self.manual_window.show()
            # self.hall = GameHallWindow(user_name, self.server_ip, auth_headers, self.login_hook)
            # self.hall.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Error', 'Unexisted user or wrong password')

    @pyqtSlot()
    def handle_signup(self):
        """handle clicking signup button"""
        # print("Clicked")
        user_name = self.user_name_input.text().strip()
        password = self.pwd_input.text()
        if len(user_name) < 3:
            _ = QMessageBox.question(self, 'Info', 'User name must longer than 3.\n (leading and ending spaces will be removed)',
                                     QMessageBox.Ok, QMessageBox.Ok)
            return
        if len(password) < 2:
            _ = QMessageBox.question(self, 'Info', 'Password must longer than 2.\n (leading and ending spaces will be removed)',
                                     QMessageBox.Ok, QMessageBox.Ok)
            return
        #authenticate from server side
        payload = {}
        payload["userName"] = user_name
        payload["pass"] = password
        #payload = {'user':'user', 'pass':'123456'}
        res = requests.post('http://' + self.server_ip + ':8080/auth/signup', json=payload)
        print(res.text)

        print(payload["userName"])

        if res.text == "Success":
            #tm.showinfo("Login info", "Welcome: " + username)
            #os.system('python3 showchessboard2.py')
            #sys.exit()
            QMessageBox.warning(self, 'Sign up info', 'Sign Up Success')
            #tm.showerror("Sign up info", "Sign Up Success")
        else:
            QMessageBox.warning(self, 'Signup error', 'Username already exists')
            #tm.showerror("Signup error", "Try Again")

    def login_hook(self):
        self.show()

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 't':
            print('#### Test mode: local server')
            APP = QApplication(sys.argv)
            EX = Window(server_ip="localhost")
            sys.exit(APP.exec_())
        elif sys.argv[1] == 'p' and len(sys.argv) > 2:
            print('#### Test mode: ' + sys.argv[2])
            APP = QApplication(sys.argv)
            EX = Window(server_ip=sys.argv[2])
            sys.exit(APP.exec_())
        else:
            print('Forgot server ip.')
    else:
        APP = QApplication(sys.argv)
        EX = Window()
        sys.exit(APP.exec_())
    
