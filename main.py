from ui import Ui_App
from dashboardUI import UI_Dashboard
import os
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QLabel, QMainWindow, QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets,QtSql
from PyQt5 import QtWidgets, uic, QtCore

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import firestore
cred = credentials.Certificate("firebaseAccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

class MainApplication(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_App()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.show()
        # self.Login_App = Login()
        # self.Login_App.show()
        self.ui.pushButton.clicked.connect(lambda : self.functionLogin())
        self.ui.CloseBtn.clicked.connect(self.close)
        self.ui.MinimunBtn.clicked.connect(self.showMinimized)
        self.ui.logoutButton.clicked.connect(lambda: self.functionLogout())
    def functionLogin(self):
        global mail
        Email=''
        page = auth.list_users()
        while page:
            for user in page.users:
                if(self.ui.Email.text() == user.email):
                    #print(user.email)
                    mail = Email
                    Email = user.email
                    break
            page=page.get_next_page()
        passwords=''
        if(not Email):
            print('error')
        else:
            passwords = db.collection('account').document(Email).get().get("pass")
            if(passwords == self.ui.password.text()):
                self.ui.widget.hide()
                self.ui.dashboard.show()
                name = db.collection('account').document(Email).get().get("name")
                self.ui.nameInfor.setText(name)
                print("login successful")
    def showPass(self):
        self.ui.Hidepassword.show()
        self.ui.Showpassword.hide()
        self.ui.password.setEchoMode(QtWidgets.QLineEdit.Normal)        
    def hidePass(self):
        self.ui.Hidepassword.hide()
        self.ui.Showpassword.show()
        self.ui.password.setEchoMode(QtWidgets.QLineEdit.Password)
    def functionLogout(self):
        self.ui.dashboard.close()
        self.ui.widget.show()


#         # self.openDB()
#     # def openDB(self):
#     #     self.db=QtSql.QSqlDatabase.addDatabase("QSQLITE")
#     #     self.db.setDatabaseName("accLogin.sqlite")
#     #     if not self.db.open():
#     #         print("error")
#     #     self.query = QtSql.QSqlQuery()
      

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    w = MainApplication()
    sys.exit(app.exec_())

