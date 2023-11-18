import os,sys

import mysql
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QLabel, QPushButton, QCheckBox, QSpinBox, QFrame, QWidget,
                             QHBoxLayout, QVBoxLayout, QFormLayout, QMainWindow, QApplication, QTabWidget,
                             QLineEdit, QRadioButton, QGroupBox, QComboBox, QTableWidget, QTextEdit, QDateEdit,
                             QTableWidgetItem, QMessageBox)

from PyQt5.QtGui import QFont
from mysql.connector import Error


from audit import Audit
#from login import login
from commonauth import User
#from mainmenu import mainmenu
class payments(QWidget):
    def __init__(self,audit):
        super().__init__()
        self.audit = audit
        print("Audit:",self.audit)
        self.initUi()
    #widgets
    def initUi(self):

        #Payment Ui
        self.resize(400, 300)
        form1 = QFormLayout()

        self.customerID_lne = QLineEdit()
        self.customerID_lne.setFixedWidth(300)
        customerID_lbl = QLabel("Customer ID")
        cardnumber_lbl = QLabel("Card no:")
        self.cardnumber_lne = QLineEdit()
        self.cardnumber_lne.setFixedWidth(300)
        expirydate_lbl = QLabel("Expiry date")
        self.expirydate_lne = QLineEdit()
        self.expirydate_lne.setFixedWidth(300)

        cardtype_lbl = QLabel("Card type")

        self.master_qrb = QRadioButton("Master")
        self.visa_qrb = QRadioButton("Visa")
        cvv_lbl = QLabel("CVV")
        self.cvv_lne = QLineEdit()
        self.cvv_lne.setFixedWidth(300)
        submit_btn = QPushButton("Submit")
        submit_btn.setFixedWidth(100)
        submit_btn.clicked.connect(self.saveToDB)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedWidth(100)
        cancel_btn.clicked.connect(self.cancel_btn)
        cashpayment = QLabel("Cash Payment")
        amount_lbl = QLabel("Amount")
        self.amount_lne = QLineEdit()
        self.amount_lne.setFixedWidth(300)
        total_lbl = QLabel("Total")
        self.total_lne = QLineEdit()
        self.total_lne.setFixedWidth(300)
        comments_qtb = QTextEdit()
        comments_qtb.resize(400,400)
        mainmenu_btn = QPushButton("Main Menu")
        printReceipt_btn = QPushButton("Print")
        printReceipt_btn.setFixedWidth(100)

        form1.addRow(customerID_lbl, self.customerID_lne)
        form1.addRow(cardnumber_lbl, self.cardnumber_lne)
        form1.addRow(expirydate_lbl, self.expirydate_lne)
        form1.addRow(cardtype_lbl)
        form1.addRow(self.master_qrb, self.visa_qrb)
        form1.addRow(cvv_lbl, self.cvv_lne)

        form1.setVerticalSpacing(20)
        form1.addRow(amount_lbl,self.amount_lne)
        form1.addRow(submit_btn, cancel_btn)
        form1.addRow(comments_qtb)
        form1.addRow(mainmenu_btn,printReceipt_btn)

        # Tab 1 layout
        tab1_layout = QVBoxLayout()
        groupbox = QGroupBox("Payment details")
        groupbox.setLayout(form1)
        tab1_layout.addWidget(groupbox)

        # Tab 2 layout
        displayEdit_btn = QPushButton("Display")
        displayEdit_btn.setFixedWidth(300)
        displayEdit_btn.clicked.connect(self.getData)
        self.searchEdit_lne = QLineEdit()
        self.searchEdit_lne.setFixedWidth(300)
        nameEdit_lne = QLineEdit()
        nameEdit_lne.setFixedWidth(300)
        surnameEdit_lne = QLineEdit()
        surnameEdit_lne.setFixedWidth(300)
        idEdit_lne = QLineEdit()
        idEdit_lne.setFixedWidth(300)
        comments_lbl = QLabel("Historical Payments")
        quitEdit_btn = QPushButton("Quit")
        quitEdit_btn.setFixedWidth(100)
        search_btn_history= QPushButton("Search")
        search_btn_history.clicked.connect(self.searchID)

        tab2_layout = QVBoxLayout()
        form2 = QFormLayout()
        self.displayPayments_qwt = QTableWidget()
        self.displayPayments_qwt.setColumnCount(6)
        self.displayPayments_qwt.setHorizontalHeaderLabels(
            ['customers_cust_id','card_no','card_expire','card_type','cvv','amount'])
        self.displayPayments_qwt.horizontalHeader().setStretchLastSection(True)
        form2.addRow(displayEdit_btn)
        form2.addRow(comments_lbl)
        form2.addRow(self.displayPayments_qwt)
        form2.addRow(search_btn_history,self.searchEdit_lne)

        form2.setVerticalSpacing(10)

        groupboxHistory = QGroupBox("History")
        groupboxHistory.setLayout(form2)
        tab2_layout.addWidget(groupboxHistory)

        # Tab widget
        tabs = QTabWidget()
        tabs.addTab(QWidget(), "Add Payment")
        tabs.addTab(QWidget(), "History Payments")

        tabs.widget(0).setLayout(tab1_layout)
        tabs.widget(1).setLayout(tab2_layout)

        # Main layout
        main_layout = QFormLayout()
        main_layout.addRow(tabs)
        self.setLayout(main_layout)

        self.setWindowTitle("Payment Screen")
        self.setGeometry(100, 100, 1200, 900)
        self.setFixedSize(1200, 900)

    @pyqtSlot()
    def cancel_btn(self):
        crn = self.cardnumber_lne.text()
        amt = self.amount_lne.text()
        access_log = "pmt_screen"

        user = self.audit

        print("user:",user)
        auditlog="crn:" +crn +" amt:" +"R"+amt
        print(auditlog)

        cnx = mysql.connector.connect(user='bee', password='P@ssword', host='localhost',
                                      auth_plugin='mysql_native_password', database='hmsdb')

        cursor = cnx.cursor()

        userlog_query = "SELECT nameofuser,userroles FROM users WHERE username =%s"
        cursor.execute(userlog_query,(user,))
        result=cursor.fetchall()


        for item in result:
            self.nameofuser = item[0]
            print("nameofuser:" + self.nameofuser)
            self.userrole = item[1]
            print("userrole:" + self.userrole)

        log_query="INSERT INTO audit_log (username,nameofuser,accessrole,screenaccess,useraction) VALUES (%s,%s,%s,%s,%s)"

        result =cursor.execute(log_query, (user,self.nameofuser, self.userrole,access_log,auditlog))
        cnx.commit()
        print("Save button query:",result)

        if crn and amt is not None:
            print("Cancel Button + username: ",user)
        else:
            print("No values entered for CRN and AMT")


    @pyqtSlot()
    def saveToDB(self):
        try:
            crn = self.cardnumber_lne.text()
            amt = self.amount_lne.text()
            access_log = "pmt_screen"

            user = self.audit

            print("user:", user)
            auditlog = "crn:" + crn + " amt:" + "R" + amt
            print(auditlog)

            cnx = mysql.connector.connect(user='bee', password='P@ssword', host='localhost',
                                      auth_plugin='mysql_native_password', database='hmsdb')

            cursor = cnx.cursor()

            userlog_query = "SELECT nameofuser,userroles FROM users WHERE username =%s"
            cursor.execute(userlog_query, (user,))
            result = cursor.fetchall()

            for item in result:
                self.nameofuser = item[0]
                print("nameofuser:" + self.nameofuser)
                self.userrole = item[1]
                print("userrole:" + self.userrole)

            log_query = "INSERT INTO audit_log (username,nameofuser,accessrole,screenaccess,useraction) VALUES (%s,%s,%s,%s,%s)"

            result = cursor.execute(log_query, (user, self.nameofuser, self.userrole, access_log, auditlog))
            cnx.commit()
            print("Save button query:", result)


            if crn and amt is not None:
                print("Cancel Button + username: ", user)
            else:
                print("No values entered for CRN and AMT")

            # Get payment amount from the input
            amount = int(self.amount_lne.text())
            # display total in total lineedit
            total = (int(self.amount_lne.text()) * 0.14) + int(self.amount_lne.text())
            print('total:', total)
            convtotal = str(total)
            finaltotal = self.total_lne.setText(convtotal)
            self.total_lne.setText(finaltotal)

            cursor = cnx.cursor()
            # We get the actual id of the customer [look in customers and enter the idnumber]

            sql = "SELECT cust_id FROM customers WHERE id_number=%s"
            # sql = "SELECT cust_id FROM customers WHERE id_number = 12345"

            customer_id = self.customerID_lne.text()

            cursor.execute(sql,(customer_id,))

            result = cursor.fetchone()
            print(result)
            if result is not None:
                cust_id = result[0]
                print("cust_id",cust_id)

                amount = int(self.amount_lne.text())

                print('Amount', amount)

                self.cardtype = "Master" if self.master_qrb.isChecked() else "Visa"

                # Insert the payment record into the "payments" table
                sql = "INSERT INTO payments (customers_cust_id,card_no,card_expire,card_type,cvv,amount) VALUES (%s, %s, %s, %s, %s, %s)"
                '''values = (self.customerID_lne.text(), self.cardnumber_lne.text(), self.expirydate_lne.text(), self.cardtype,
                      self.cvv_lne.text(), amount)'''
                values = (cust_id, self.cardnumber_lne.text(), self.expirydate_lne.text(), self.cardtype,self.cvv_lne.text(), amount)
                cursor.execute(sql, values)
                cnx.commit()

        except mysql.connector.Error as err:
            #Handle MySQL errors
            error_msg = f"MySQL Error: {err}"
            QMessageBox.critical(self, "Error", error_msg)

        except Exception as e:
            # Handle other exceptions
            error_msg = f"An error occurred: {e}"
            QMessageBox.critical(self, "Error", error_msg)
            print(error_msg)

        finally:
            cursor.close()
            cnx.close()

    @pyqtSlot()
    def getData(self):
        print('Get Data Clicked!!!')
        try:
            print("getdata button clicked!!!")
            #search_term = self.search_lne.text()
            #print(search_term)
            cnx = mysql.connector.connect(user='bee', password='P@ssword',
                                          host='localhost', auth_plugin='mysql_native_password', database='hmsdb')
            cursor = cnx.cursor()

            # Check if username and password exist in database

            search_query = "SELECT customers_cust_id,card_no,card_expire,card_type,cvv,amount FROM payments"

            cursor.execute(search_query)
            result = cursor.fetchall()
            print(result)
            self.displayPayments_qwt.setRowCount(len(result))

            for row_idx, row in enumerate(result):
                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value))

                    self.displayPayments_qwt.setItem(row_idx, col_idx, item)
                    print(row_idx, col_idx, item, value)

            # To build an option to display all records later and fix error handling

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
            print("Generated SQL query:", search_query)

    @pyqtSlot()
    def searchID(self):
        print("search id clicked")
        try:
            print("search id button clicked!!!")
            search_term = self.searchEdit_lne.text()
            print(search_term)
            cnx = mysql.connector.connect(user='bee', password='P@ssword',
                                          host='localhost', auth_plugin='mysql_native_password', database='hmsdb')
            cursor = cnx.cursor()

            search_query = "SELECT customers_cust_id,card_no,card_expire,card_type,cvv,amount FROM payments WHERE customers_cust_id = %s"

            cursor.execute(search_query, (search_term,))
            result = cursor.fetchall()
            print(result)
            self.displayPayments_qwt.setRowCount(len(result))

            for row_idx, row in enumerate(result):
                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value))

                    self.displayPayments_qwt.setItem(row_idx, col_idx, item)
                    print(row_idx, col_idx, item, value)
            if search_term == "":
                error_msg = "Enter a name or surname or id"
                QMessageBox.critical(self, "Error", error_msg)

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
            print("Generated SQL query:", search_query)

if __name__=='__main__':
    app=QApplication(sys.argv)
    window=payments()
    window.show()
    sys.exit(app.exec_())