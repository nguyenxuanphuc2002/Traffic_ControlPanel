from PyQt5 import QtWidgets, QtCore, QtSql, uic
from loginUi import Ui_Form
import loginUi 
from dashboardUI import Ui_dashboard
import sys

#firebase
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore 

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

db = firestore.client()

email = input("Đăng ký tài khoản: ")
password = input("Mật khẩu: ")

user = auth.create_user_with_email_and_password(email,password)
token = user['localId']
print(token)
db.collection('users').document(token).set({'email': email, 'password': password})