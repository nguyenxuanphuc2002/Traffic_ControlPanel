import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

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

def vehicleError(licencePlate, error, time_utc = None ):
    """Dùng để bắn thông tin vi phạm giao thông thu được từ camera lên trên cloud Firestore
    
    Args:
        licensePlate: lấy thông tin biển số xe dưới dạng string
        error: lấy thông tin lỗi vi phạm dưới dạng string
        time_utc: lấy thông tin về thời gian lúc phương tiện vi phạm giao thông dưới dạng timestamp
            (optional): người dùng có thể đưa vào thông tin về thời gian theo ý muốn, nếu không đưa vào
            thì trình sẽ tự lập thời gian theo thời gian UTC hiện tại"""
    plate = licencePlate
    error_ = error
    if time_utc != None:
        time_ = time_utc
    else:
        time_utc = datetime.now()
    db.collection('Vipham').add({'License plate': plate,'Error': error_,'Time': time_utc})

biensoxe = input("Nhập biển số xe: ")
vipham = input("Nhập lỗi vi phạm: ")
vehicleError(biensoxe,vipham)
