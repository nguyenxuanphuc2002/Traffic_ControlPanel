from PyQt5 import QtWidgets, QtCore, QtSql
from loginUi import Ui_Form
import loginUi
from dashboardUI import Ui_dashboard
import sys

#firebase
import pyrebase
import firebase_admin
from firebase_admin import credentials
cred = credentials.Certificate("serviceAccountKey.json")
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

class dashboardApp(QtWidgets.QMainWindow, Ui_dashboard):
    def signOut(self):
            self.window = QtWidgets.QWidget()
            self.ui = Ui_Form()
            self.ui.setupUi(self.window)
            print("logout")
            dashboard.hide()
            self.window.show()
    def clicked(self):
        print("clicked")

    def __init__(self):
        super(dashboardApp, self).__init__()
        self.setupUi(self)

        self.logOut_btn.clicked.connect(self.signOut)
        self.pushButton.clicked.connect(self.clicked)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dashboard = dashboardApp()
    dashboard.show()
    sys.exit(app.exec_())
   