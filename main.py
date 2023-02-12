from ui import Ui_App
# from dashboardUI import UI_Dashboard
import os
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QLabel, QMainWindow, QTableWidget
from PyQt5 import QtCore, QtGui, QtWidgets,QtSql
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QHeaderView

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import firestore
cred = credentials.Certificate("firebaseAccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

import pyrebase
firebaseConfig={
    'apiKey': "AIzaSyC3yZ0EGATbE1xLFL9h2JTJXhhw2ISY2-M",
    'authDomain': "demodb-b3cc8.firebaseapp.com",
    'projectId': "demodb-b3cc8",
    'storageBucket': "demodb-b3cc8.appspot.com",
    'messagingSenderId': "790501299589",
    'appId': "1:790501299589:web:737dddcdfc55e90d4ce0ec",
    'measurementId': "G-DBB3ZL0KB0",
     'databaseURL': ""
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

class MainApplication(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_App()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.show()
        # self.Login_App = Login()
        # self.Login_App.show()
        self.ui.pushButton.clicked.connect(lambda : self.functionLogin())
        self.ui.closeBtn.clicked.connect(self.close)
        self.ui.minimizeBtn.clicked.connect(self.showMinimized)
        self.ui.logoutBtn.clicked.connect(lambda: self.functionLogout())
        self.ui.chartPage.clicked.connect(lambda: self.changeTab(1))
        self.ui.listcamPage.clicked.connect(lambda: self.changeTab(2))

    def functionLogin(self):
        global Email
        Email = self.ui.Email.text()
        passwords = self.ui.password.text()
        # if(not Email):
        #     print('error')
        # else:
        #     passwords = db.collection('account').document(Email).get().get("pass")
        #     if(passwords == self.ui.password.text()):
        #         self.ui.widget.hide()
        #         self.ui.dashboard.show()
        #         name = db.collection('account').document(Email).get().get("name")
        #         self.ui.nameInfor.setText(name)
        #         print("login successful")
        try:
            auth.sign_in_with_email_and_password(Email,passwords)
            # self.accept()
            print("login successful!")
            self.ui.widget.hide()
            self.ui.dashboard.show()
            self.showUserInfo()
            self.loadData()
        except:
            print('error')

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

    # def showThongke(self):
    #     self.ui.thongke.show()
    #     self.loadData()
        
        
    def loadData(self):
        query = db.collection('Vipham').get()

        data = [ i.to_dict() for i in query]
        data = [
            {k:v.rfc3339() if k=="Time" else v for k,v in item.items()}
            for item in data
        ]
        self.ui.violationTableWidget.setRowCount(0)
        print(data)
        for row_number, row_data in enumerate(data):
            self.ui.violationTableWidget.insertRow(row_number)
            for col_number, value in enumerate(row_data.items()):
                # print(col_number)
                # print(type(col_number))
                # print(value)
                # print(type(value[1]))
                self.ui.violationTableWidget.setItem(row_number, col_number, QtWidgets.QTableWidgetItem(value[1]))

        header = self.ui.violationTableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
 
    def showUserInfo(self):
        docs = db.collection('users').where("email", "==", Email).get()
        for doc in docs:
            data = doc.to_dict()
            name = data["Name"]
            self.ui.nameInfo.setText(name)
        self.ui.emailLabel.setText(Email)
        

    def changeTab(self,index):
        if index == 0:
            self.ui.dashboard_Tab.setCurrentIndex(0)
        elif index == 1:
            self.ui.dashboard_Tab.setCurrentIndex(1)
        elif index == 2:
                    self.ui.dashboard_Tab.setCurrentIndex(2)                  

    # def set_transparency(self, enabled):
    # if enabled:
    #     self.setAutoFillBackground(False)
    # else:
    #     self.setAttribute(Qt.WA_NoSystemBackground, False)

    # self.setAttribute(Qt.WA_TranslucentBackground, enabled)
    # self.repaint()

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

