import os,sys

#from PyQt5.QtCore.QProcess import state
from PyQt5.QtWidgets import (QWidget,QApplication,
                             QLabel,QLineEdit,QPushButton,QCheckBox,
                             QFrame,QMessageBox)

from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot, Qt
import mysql
import mysql.connector
from mysql.connector import connect, Error
from mainmenu import mainmenu
from commonauth import User
from audit import Audit
from payments import payments

class globally_logged_class:
    global_username=""

class login(QWidget):
    def __init__(self):
        super().__init__()

    #widgets
        self.appname_lbl=QLabel(self)
        self.usrname_lbl=QLabel(self)
        self.usrname_lne=QLineEdit(self)
        self.password_lbl=QLabel(self)
        self.password_lne=QLineEdit(self)
        self.showpassword_chb=QCheckBox(self)
        self.showpassword_lbl=QLabel(self)

        self.forgotchangepass_lbl=QLabel(self)
        self.loginframe_qf= QFrame(self)
        self.logo_pm=QPixmap('HMS_logo.jpg')
        self.logo =QLabel(self)
        self.version_lbl=QLabel(self)
        self.helplink_lbl=QLabel(self)
        self.authAlert_messg=QMessageBox()

    #functions
        self.drawWindow()
        self.initWidgets()
        self.authenticateDB()

    def initWidgets(self):
        self.logo.setPixmap(self.logo_pm)
        self.logo.resize(150,100)
        self.logo.move(335,120)
        self.logo.setFixedWidth(400)

        self.appname_lbl.setText("Hotel Management System")
        self.appname_lbl.move(320,70)
        self.appname_lbl.setFont(QFont('Arial',12))
        self.appname_lbl.setFixedWidth(350)

        self.usrname_lbl.setFont(QFont('Arial', 12))
        self.usrname_lbl.setText("username:")
        self.usrname_lbl.move(200,250)
        self.usrname_lbl.setFixedWidth(300)
        self.usrname_lne.setPlaceholderText("type username")
        self.usrname_lne.move(320,245)
        self.usrname_lne.setFixedWidth(250)
        self.password_lbl.setText("password:")
        self.password_lbl.setFont(QFont('Arial', 12))
        self.password_lbl.move(200,320)
        self.password_lbl.setFixedWidth(300)
        self.password_lne.setPlaceholderText("type password")
        self.password_lne.move(320,315)
        self.password_lne.setFixedWidth(250)

        self.loginframe_qf.setFrameShape(QFrame.StyledPanel)

        self.loginframe_qf.resize(400,500)
        self.loginframe_qf.move(190,30)
        self.forgotchangepass_lbl.setText("Forgot username or password?")
        self.forgotchangepass_lbl.setFixedWidth(300)
        self.forgotchangepass_lbl.setStyleSheet("QLabel {color : blue;}")
        self.forgotchangepass_lbl.move(350,490)

        self.login_btn = QPushButton(self)
        self.login_btn.clicked.connect(self.authenticateDB)
        self.login_btn.setText("Login")
        self.login_btn.move(320,400)
        self.login_btn.setFixedSize(100,50)

        self.quit_btn = QPushButton(self)
        self.quit_btn.setText("Quit")
        self.quit_btn.move(470,400)
        self.quit_btn.setFixedSize(100,50)
        self.quit_btn.clicked.connect(self.closeProgram)
        self.version_lbl.setText("Version 1.0")
        self.version_lbl.setFont(QFont('Arial',7))
        self.version_lbl.move(700,600)
        self.version_lbl.setFixedWidth(100)
        self.helplink_lbl.setText("Help")
        self.helplink_lbl.move(20,600)
        self.helplink_lbl.setFixedWidth(100)

    def drawWindow(self):
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle("Login")
        self.setFixedSize(800, 640)

    def logged_in_globaluser(self):
        globally_logged_class.global_username=self.usrname_lne.text()
        return globally_logged_class

    @pyqtSlot()
    def authenticateDB(self):

       try:
            self.username = self.usrname_lne.text()
            self.password_lne.setEchoMode(QLineEdit.Password)

            self.password = self.password_lne.text()
            #create instance variable to pass to mainmenu class

            user = User(self.username)

            cnx = mysql.connector.connect(user='bee', password='P@ssword',
                                          host='localhost',auth_plugin='mysql_native_password', database='hmsdb')
            cursor = cnx.cursor()

            # Check if username and password exist in database
            query = "SELECT * FROM users WHERE username = %s AND passwords = %s"
            cursor.execute(query,(self.username,self.password))
            result = cursor.fetchone()
            if result:
                self.mainmenuWindow = mainmenu(user)
                self.audit_to_payment = Audit(user)
                self.mainmenuWindow.show()
                self.close()

            elif result=='':
                # Failed login
                QMessageBox.warning(self, 'Error', 'Invalid username or password.')

       except mysql.connector.Error as err:
           # Handle MySQL errors
           error_msg = f"MySQL Error: {err}"
           QMessageBox.critical(self, "Error", error_msg)

       except Exception as e:
            # Handle other exceptions
            error_msg = f"An error occurred: {e}"
            QMessageBox.critical(self, "Error", error_msg)
       finally:
            cursor.close()
            cnx.close()
            print("Generated SQL query:")

    def closeProgram(self):
        self.close()

#start program
if __name__ =='__main__':
    app=QApplication(sys.argv)
    window=login()
    window.show()
    sys.exit(app.exec_())

