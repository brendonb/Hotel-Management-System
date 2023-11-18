import sys,os

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QLineEdit, QPushButton,
                             QHBoxLayout, QFormLayout, QVBoxLayout, QFrame, QMessageBox)
from PyQt5.QtGui import (QFont,QPixmap)

#from customerinfo import Customers
#from customerinfo_Copy import Customers

from audit import Audit
from rooms import rooms
from payments import payments
from waitlist import waitlist
from analytics import analytics
from reports import reports
from systemmenu import systemmenu
from customerinfo import *
from commonauth import User

class mainmenu(QWidget):
    def __init__(self,user):
        super().__init__()
        self.user = user

        #declare widgets
        self.appname_lbl=QLabel(self)
        self.logo_qp=QPixmap('HMS_logo.jpg')
        self.logo_lbl=QLabel(self)

        self.helplink_lbl = QLabel(self)
        self.version_lbl= QLabel(self)
        self.mainmenu_qf =QFrame(self)
        self.submenuusr_qf=QFrame(self)
        self.submenuadmin_qf=QFrame(self)

        self.hbox = QHBoxLayout()
        self.fbox = QFormLayout()
        self.vbox = QVBoxLayout()

        #declare functions
        self.displayWindow()
        self.windowLayoutManager()
        self.initWidgets()
        #run functions

    def displayWindow(self):
        self.setWindowTitle("Main Menu")
        self.setFixedSize(1024,800)

    def windowLayoutManager(self):
        None
    def initWidgets(self):
        self.appname_lbl.setText("Hotel Management System")
        self.appname_lbl.setFixedWidth(300)
        self.appname_lbl.move(405,70)
        self.appname_lbl.setFont(QFont('Arial',12))
        self.logo_lbl.setPixmap(self.logo_qp)
        self.logo_lbl.resize(150,100)
        self.logo_lbl.setFixedWidth(400)
        self.logo_lbl.move(450,100)

        self.mainmenu_qf.setFrameShape(QFrame.StyledPanel)
        self.mainmenu_qf.resize(900,700)
        self.mainmenu_qf.move(65,50)

        self.submenuusr_qf.setFrameShape(QFrame.StyledPanel)
        self.submenuusr_qf.resize(300,500)
        self.submenuusr_qf.move(150,200)

        self.submenuadmin_qf.setFrameShape(QFrame.StyledPanel)
        self.submenuadmin_qf.resize(300,500)
        self.submenuadmin_qf.move(600,200)

        self.customerinfo_btn = QPushButton(self)
        self.customerinfo_btn.clicked.connect(self.openCustomer_menu)
        self.customerinfo_btn.setText("Customers")
        self.customerinfo_btn.resize(200,100)
        self.customerinfo_btn.move(207,220)

        self.rooms_btn = QPushButton(self)
        self.rooms_btn.clicked.connect(self.openRooms_menu)
        self.rooms_btn.setText("Rooms")
        self.rooms_btn.resize(200,100)
        self.rooms_btn.move(207,340)

        self.payments_btn = QPushButton(self)
        self.payments_btn.clicked.connect(self.openPayments_menu)
        self.payments_btn.setText("Payments")
        self.payments_btn.resize(200,100)
        self.payments_btn.move(207,460)

        self.waitlist_btn = QPushButton(self)
        self.waitlist_btn.clicked.connect(self.openWaitlist_menu)
        self.waitlist_btn.setText("Wait List")
        self.waitlist_btn.resize(200, 100)
        self.waitlist_btn.move(207, 580)

        self.analysis_btn = QPushButton(self)
        self.analysis_btn.clicked.connect(self.openAnalytics_menu)
        self.analysis_btn.setText("Analytics")
        self.analysis_btn.resize(200,100)
        self.analysis_btn.move(652,220)

        self.reports_btn = QPushButton(self)
        self.reports_btn.clicked.connect(self.openReports_menu)
        self.reports_btn.setText("Reports")
        self.reports_btn.resize(200,100)
        self.reports_btn.move(652,340)

        self.systemmenu_btn = QPushButton(self)
        self.systemmenu_btn.clicked.connect(self.openSystem_menu)
        self.systemmenu_btn.setText("System")
        self.systemmenu_btn.resize(200,100)
        self.systemmenu_btn.move(652,460)

        self.exit_btn = QPushButton(self)
        self.exit_btn.setText("Exit")
        self.exit_btn.resize(200,100)
        self.exit_btn.move(652,580)

        self.helplink_lbl.setText("Help")
        self.helplink_lbl.setFixedWidth(100)
        self.helplink_lbl.move(70,730)

        self.version_lbl.setText("Version 1.0")
        self.version_lbl.setFixedWidth(100)
        self.version_lbl.move(880,730)

        cnx = mysql.connector.connect(user='bee', password='P@ssword',
                                      host='localhost', auth_plugin='mysql_native_password', database='hmsdb')
        cursor = cnx.cursor()

        self.perm_username = self.user.get_username()
        perm_query = "SELECT customerscreen,paymentscreen,analyticsscreen,systemsscreen,roomscreen,waitlistscreen,reportsscreen FROM acl WHERE users_username=%s"
        cursor.execute(perm_query, (self.perm_username,))
        perm_result = cursor.fetchall()

        #loop through db ,and set permissions
        for items in perm_result:
            self.customerscreen = items[0]
            self.paymentsscreen = items[1]
            self.analyticssreen = items[2]
            self.systemsscreen = items[3]
            self.roomsscreen = items[4]
            self.waitlistscren = items[5]
            self.reportsscreen = items[6]
            print("Customer Screen", self.customerscreen)

        cursor.close()
        cnx.close()

    @pyqtSlot()
    def openCustomer_menu(self):

        if self.customerscreen == "yes":
            #self.customerinfo_Copy = Customers()
            self.customerinfo_Copy = Customers()
            self.customerinfo_Copy.show()

    @pyqtSlot()
    def openRooms_menu(self):
        if self.roomsscreen == "yes":
            self.roomsWindow = rooms()
            self.roomsWindow.show()
        else:
            QMessageBox.warning(self, 'Error', 'Access Denied!!!.')
            self.roomsWindow.close()
        print("clicked rooms button")
    @pyqtSlot()
    def openPayments_menu(self):
        perm_username = self.user.get_username()
        self.paymentsWindow = payments(perm_username)

        self.audit_to_payment = Audit(perm_username)

        print("Perm_-username", perm_username)

        if self.paymentsscreen == "yes":

            self.paymentsWindow.show()

        else:
            QMessageBox.warning(self, 'Error', 'Access Denied!!!.')
            self.paymentsWindow.close()

    @pyqtSlot()
    def openWaitlist_menu(self):
        if self.waitlistscren == "yes":
            mainmenu.openWaitlist_menu()
            self.waitlistWindow = waitlist()
            self.waitlistWindow.show()
        else:
            QMessageBox.warning(self, 'Error', 'Access Denied!!!.')
            self.waitlistWindow.close()
        print("clicked waitlist button")

    @pyqtSlot()
    def openAnalytics_menu(self):
        if self.analyticssreen == "yes":
            self.analyticsWindow=analytics()
            self.analyticsWindow.show()
        else:
            QMessageBox.warning(self, 'Error', 'Access Denied!!!.')
            self.analyticsWindow.close()
        print("clicked analytics button")

    @pyqtSlot()
    def openReports_menu(self):
        if self.reportsscreen == "yes":
            self.reportsWindow = reports()
            self.reportsWindow.show()
        else:
            QMessageBox.warning(self, 'Error', 'Access Denied!!!.')
            self.reportsWindow.close()
        print("clicked reports button")

    @pyqtSlot()
    def openSystem_menu(self):
        if self.systemsscreen == "yes":
            self.systemWindow = systemmenu()
            self.systemWindow.show()
        else:
            QMessageBox.warning(self, 'Error', 'Access Denied!!!.')
            self.systemWindow.close()
        print("clicked system button")

    #start program
if __name__=='__main__':
    app=QApplication(sys.argv)
    mainmenu_window= mainmenu()
    mainmenu_window.show()
    sys.exit(app.exec_())
