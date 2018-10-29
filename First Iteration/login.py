import requests
import json
import os
from tkinter import *
import tkinter.messagebox as tm
from showchessboard3 import *

class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.checkbox = Checkbutton(self, text="Keep me logged in")
        self.checkbox.grid(columnspan=2)

        self.logbtn = Button(self, text="Login", command=self._login_btn_clicked)
        self.signupbtn = Button(self, text="Sign Up", command=self._sign_up_btn_clicked)
        self.logbtn.grid(columnspan=2)
        self.signupbtn.grid(columnspan=2)

        self.pack()

    def _login_btn_clicked(self):
        # print("Clicked")
        username = self.entry_username.get()
        password = self.entry_password.get()
        #authenticate from server side
        payload = {}
        payload["userName"] = username
        payload["pass"] = password
        #payload = {'user':'user', 'pass':'123456'}
        r = requests.post('http://localhost:8080/auth/login', json=payload)

        print(r.text)
        print(payload)
        print(payload["userName"])

        if r.text == "Success":
            tm.showinfo("Login info", "Welcome: " + username)
            #os.system('python3 showchessboard2.py')
            #self.quit()
            game = Gomoku()
            game.show()
            sys.exit(app.exec_())
            #sys.exit()

        else:
            tm.showerror("Login error", "Incorrect username")

    def _sign_up_btn_clicked(self):
        # print("Clicked")
        username = self.entry_username.get()
        password = self.entry_password.get()
        #authenticate from server side
        payload = {}
        payload["userName"] = username
        payload["pass"] = password
        #payload = {'user':'user', 'pass':'123456'}
        r = requests.post('http://localhost:8080/auth/signup', json=payload)
        print(r.text)
        
        print(payload["userName"])

        if r.text == "Success":
            #tm.showinfo("Login info", "Welcome: " + username)
            #os.system('python3 showchessboard2.py')
            #sys.exit()
            tm.showerror("Sign up info", "Sign Up Success")
        else:
            tm.showerror("Signup error", "Try Again")


# root = Tk()
# lf = LoginFrame(root)
# root.mainloop()

