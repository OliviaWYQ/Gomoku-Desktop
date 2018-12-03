"""
Entrance of the project, login& signup window
"""

import sys
#from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QMessageBox, QApplication
from PyQt5.QtGui import QIcon
import requests
from manual import *
from hall import GameHallWindow

#IP = "localhost"
IP = "52.207.232.53"

class Window(QMainWindow):
    """Log in window"""

    def __init__(self):
        super().__init__()
        self.title = "Gomoku"
        self.top = 330
        self.left = 100
        self.width = 600
        self.height = 500
        self.init_ui()

    def init_ui(self):
        """init the window, adding buttons and inputs"""
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setWindowIcon(QIcon('chessboard/gomoku_icon.png')) # set window icon
        login_btn = QPushButton('log in', self)
        login_btn.move(100, 300)
        login_btn.clicked.connect(self.handle_login)
        self.user_name_input = QLineEdit("12345", self)
        self.user_name_input.setGeometry(100, 100, 400, 30)

        signup_btn = QPushButton('sign up', self)
        signup_btn.move(400, 300)
        signup_btn.clicked.connect(self.handle_signup)
        self.pwd_input = QLineEdit("123", self)
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.pwd_input.setGeometry(100, 200, 400, 30)
        self.pwd_input.setEchoMode(QLineEdit.Password)

        self.server_ip = QLineEdit(IP, self)
        self.server_ip.setGeometry(100, 400, 400, 30)

        self.show()

    @pyqtSlot()
    def handle_login(self):
        """handle clicking login button"""
        payload = {}
        payload["userName"] = self.user_name_input.text()
        payload["pass"] = self.pwd_input.text()
        #payload = {'user':'user', 'pass':'123456'}
        res = requests.post('http://' + self.server_ip.text() + ':8080/auth/login', json=payload)
        print(res.text)

        print(payload["userName"])

        if len(res.text)>7 and res.text[:7] == "Success":
            # user_tooken = res[6:]
            # QMessageBox.warning(self, 'Success', 'Success')
            user_name = self.user_name_input.text()
            auth_headers = {'TOKEN': res.text[8:], 'USER_NAME': user_name}
            print(auth_headers)
            self.manual_window = manual(self.user_name_input.text(), self.server_ip.text(), auth_headers, self.login_hook)
            self.manual_window.show()
            # self.hall = GameHallWindow(user_name, self.server_ip.text(), auth_headers, self.login_hook)
            # self.hall.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Error', 'Unexisted user or wrong password')

    @pyqtSlot()
    def handle_signup(self):
        """handle clicking signup button"""
        # print("Clicked")
        user_name = self.user_name_input.text()
        password = self.pwd_input.text()
        #authenticate from server side
        payload = {}
        payload["userName"] = user_name
        payload["pass"] = password
        #payload = {'user':'user', 'pass':'123456'}
        res = requests.post('http://' + self.server_ip.text() + ':8080/auth/signup', json=payload)
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
    APP = QApplication(sys.argv)
    EX = Window()
    sys.exit(APP.exec_())
