from PyQt5 import QtWidgets, QtCore, QtSql
from PyQt5.QtWidgets import QStackedWidget
import sqlite3
import loginUi 
from loginUi import Ui_Form
from dashboardUI import Ui_dashboard
import sys

#firebase
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore 

cred = credentials.Certificate("credentials/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

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

db = firestore.client()

class LoginApp(QtWidgets.QDialog, Ui_Form):
    def changeForm(self):
        if self.pushButton_7.isChecked():
            self.widget_2.hide()
            self.widget_3.show()
            self.pushButton_7.setText("<")
        else:
            self.widget_2.show()
            self.widget_3.hide()
            self.pushButton_7.setText(">")

    def showPassword(self): #Ẩn hiện password theo yêu cầu
        if self.checkBox.isChecked():
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
    
    def showRegPassword(self): #Ẩn hiện password theo yêu cầu
        if self.checkBox_2.isChecked():
            self.lineEdit_6.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.lineEdit_7.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.lineEdit_6.setEchoMode(QtWidgets.QLineEdit.Password)
            self.lineEdit_7.setEchoMode(QtWidgets.QLineEdit.Password)

    def openDB(self):
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("data.sqlite")
        if not self.db.open():
            print("Error")
        self.query = QtSql.QSqlQuery()

    def register(self):
        email = self.lineEdit_3.text()
        password = self.lineEdit_6.text()
        name = self.lineEdit_4.text()
        confirmPassword = self.lineEdit_7.text()
        if email == password == confirmPassword == '':
            print("Hãy điền thông tin vào ô trống")
            self.noFillNoti()
        elif password == confirmPassword:
            try:
                user = auth.create_user_with_email_and_password(email,password)             #Lưu tài khoản đăng ký trên Firebase Authenication
                token = user['localId']
                print(token)
                db.collection('users').document(token).set({'Name': name ,'email': email, 'password': password})   #Lưu tài khoản đăng ký trên Firebase Firestore
                self.successRegister()
            except:
                print("Tài khoản đã tồn tại hoặc điền không đúng dạng email")
                self.alreadyRegistered()                
        else:
            self.failedRegister()


############ Kiểm tra tài khoản đăng nhập trên firebase #################
    def checkUser(self):
        global username1 
        global password1
        username1 = self.lineEdit.text()
        password1 = self.lineEdit_2.text()
        print(username1, password1)
        # self.query.exec_("select * from userdata where username = '%s' and password = '%s';"%(username1, password1))
        # self.query.first()
        # if self.query.value("username") != None and self.query.value("password") != None:
        try:
            auth.sign_in_with_email_and_password(username1,password1)
            self.accept()
            print("login successful!")
            self.successLogin()
        except:
            self.failedLogin()

############################################# Các trường hợp #################################################################
    def successLogin(self):                                         # Đăng nhập Thành công
        msg = QtWidgets.QMessageBox()
        msg.setText("Đăng nhập thành công")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
        msg.exec_()
        # self.openDashboard()

    def failedLogin(self):                                          # Đăng nhập thất bại
        msg2 = QtWidgets.QMessageBox()
        msg2.setText("Incorrect ID or Password")
        msg2.setIcon(QtWidgets.QMessageBox.Information)
        msg2.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg2.setDefaultButton(QtWidgets.QMessageBox.Ok)
        msg2.exec_()

    def successRegister(self):                                      #Đăng ký tài khoản thành công
        msg = QtWidgets.QMessageBox()
        msg.setText("Bạn đã đăng ký tài khoản thành công")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
        msg.exec_()
    
    def failedRegister(self):                                       #Đăng ký tài khoản thất bại (không đúng mật khẩu)
        msg = QtWidgets.QMessageBox()
        msg.setText("Mật khẩu không trùng khớp. Hãy nhập lại mật khẩu")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def alreadyRegistered(self):                                    #Tài khoản đã tồn tại
        msg = QtWidgets.QMessageBox()
        msg.setText("Tài khoản đăng ký đã tồn tại")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def noFillNoti(self):                                               
        msg = QtWidgets.QMessageBox()
        msg.setText("Hãy điền thông tin vào ô trống")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
        msg.exec_()

###################################################################################################################################

    # def openDashboard(self):
    #     self.window = QtWidgets.QMainWindow()
    #     self.ui = Ui_dashboard()
    #     self.ui.setupUi(self.window)
    #     Form.hide()
    #     self.window.show()

    def __init__(self,*args, **kwargs):
        QtWidgets.QDialog.__init__(self,*args, **kwargs)
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.openDB()

        self.label.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))
        self.label_3.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))
        self.pushButton.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=3, yOffset=3))
        self.pushButton_6.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=3, yOffset=3))

        self.widget_3.hide()
        self.pushButton_7.clicked.connect(self.changeForm)
        self.checkBox.clicked.connect(self.showPassword)
        self.checkBox_2.clicked.connect(self.showRegPassword)
        self.pushButton.clicked.connect(self.checkUser)
        self.pushButton_6.clicked.connect(self.register)
    


class dashboardApp(QtWidgets.QMainWindow, Ui_dashboard):
    def signOut(self):
            self.window = QtWidgets.QWidget()
            self.ui = LoginApp()
            self.ui.setupUi(self.window)
            print("logout")
            dashboard.hide()
            self.window.show()

    def showInfo(self):
        docs = db.collection('users').where("email", "==", username1).get()
        for doc in docs:
            data = doc.to_dict()
            name = data["Name"]
            print(name)
            self.label_2.setText(name)
        self.label_4.setText(username1)
    
    def __init__(self,*args, **kwargs):
        QtWidgets.QMainWindow.__init__(self,*args, **kwargs)
        self.setupUi(self)
        self.logOut_btn.clicked.connect(self.signOut)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = LoginApp()
    Form.show()
    dashboard = dashboardApp()
    if Form.exec_() == QtWidgets.QDialog.Accepted:
        dashboard.showInfo()
        dashboard.show()
        Form.hide()
    sys.exit(app.exec_())
