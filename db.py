from PyQt5 import QtSql

db = QtSql.QSqlDatabase.addDatabase("QSLITE")
db.setDatabaseName("accLogin.splite")

if not db.open():
    print("Error")

query = QtSql.QSqlQuery()
query.exec_("create table accountdata (id INTEGER PRIMARY KEY AUTOINCREMENT NOT FULL, email VARCHAR(100) NOT FULL, password VARCHAR(100) NOT FULL);")
query.exec_("insert table accountdata (email.password) values('phuc@gmail.com','123456';")
query.exec_("select * from accountdata where id=1;")
query.first()
