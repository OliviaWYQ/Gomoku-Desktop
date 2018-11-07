import sys
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from showchessboard import *
import requests

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "App"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        buttonWindow1 = QPushButton('log in', self)
        buttonWindow1.move(100, 100)
        buttonWindow1.clicked.connect(self.handleLogin)
        self.userName = QLineEdit("12345", self)
        self.userName.setGeometry(250, 100, 400, 30)

        buttonWindow2 = QPushButton('sign up', self)
        buttonWindow2.move(100, 200)
        buttonWindow2.clicked.connect(self.handleSignUp)        
        self.pwd = QLineEdit("123", self)
        self.pwd.setEchoMode(QLineEdit.Password)
        self.pwd.setGeometry(250, 200, 400, 30)

        self.serverIp = QLineEdit("54.173.206.13", self)
        self.serverIp.setGeometry(250, 300, 400, 30)

        self.show()

    @pyqtSlot()
    def handleLogin(self):
    
        payload = {}
        payload["userName"] = self.userName.text()
        payload["pass"] = self.pwd.text()
        #payload = {'user':'user', 'pass':'123456'}
        r = requests.post('http://' + self.serverIp.text() + ':8080/auth/login', json=payload)
        print(r.text)
        
        print(payload["userName"])

        if (r.text == "Success"):
            QMessageBox.warning(self, 'Success', 'Success')
            self.game = Gomoku(self.userName.text(), self.serverIp.text())
            self.game.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Error', 'Bad user or password')

    @pyqtSlot()
    def handleSignUp(self):
        # print("Clicked")
        username = self.userName.text()
        password = self.pwd.text()
        #authenticate from server side
        payload = {}
        payload["userName"] = username
        payload["pass"] = password
        #payload = {'user':'user', 'pass':'123456'}
        r = requests.post('http://' + self.serverIp.text() + ':8080/auth/signup', json=payload)
        print(r.text)
        
        print(payload["userName"])

        if r.text == "Success":
            #tm.showinfo("Login info", "Welcome: " + username)
            #os.system('python3 showchessboard2.py')
            #sys.exit()
            QMessageBox.warning(self, 'Sign up info', 'Sign Up Success')
            #tm.showerror("Sign up info", "Sign Up Success")
        else:
            QMessageBox.warning(self, 'Signup error', 'Username already exists')
            #tm.showerror("Signup error", "Try Again")

if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=Window()
    sys.exit(app.exec_())
