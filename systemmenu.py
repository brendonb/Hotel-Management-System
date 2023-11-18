import sys
from datetime import datetime

import mysql
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QApplication, QWidget, QFormLayout, QLineEdit,
                             QLabel, QPushButton, QHBoxLayout, QTabWidget, QVBoxLayout, QGroupBox,
                             QRadioButton, QSpinBox, QComboBox, QDateEdit, QTableWidget, QCheckBox, QMessageBox,
                             QButtonGroup, QTableWidgetItem, QFileDialog)
import subprocess
import threading
import mysql.connector
from PyQt5.QtGui import QFont
class systemmenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(400, 300)

        # First form layout
        form1 = QFormLayout()

        personalInfo = QLabel()
        personalInfo.setFont(QFont('Arial',10))
        personalInfo.setText("User Account Info")

        self.name_lne = QLineEdit()
        self.name_lne.setFixedWidth(300)
        name_lbl = QLabel("Name")
        surname_lbl = QLabel("Surname")
        self.surname_lne = QLineEdit()
        self.surname_lne.setFixedWidth(300)
        address_lbl = QLabel("Address")
        self.address_lne = QLineEdit()
        self.address_lne.setFixedSize(300,100)

        self.gender_lbl = QLabel("Gender")
        self.gender_btn_grp = QButtonGroup()
        self.male_qrb = QRadioButton("Male")
        self.female_qrb = QRadioButton("Female")
        self.gender_btn_grp.addButton(self.male_qrb)
        self.gender_btn_grp.addButton(self.female_qrb)
        self.gender = "Male" if self.male_qrb.isChecked() else "Female"

        id_lbl = QLabel("ID no")
        self.id_lne = QLineEdit()
        self.id_lne.setFixedWidth(300)
        city_lbl = QLabel("City")
        self.city_lne = QLineEdit()
        self.city_lne.setFixedWidth(300)
        province_lbl = QLabel("Province")
        self.province_qcb = QComboBox()
        self.province_qcb.addItems(['', 'Western Cape', 'Eastern Cape', 'Northen Cape', 'Southern Cape',
                                    'Gauteng'])

        self.province_qcb.setFixedWidth(300)
        contacInfo_lbl = QLabel()
        contacInfo_lbl.setFont(QFont('Arial', 10))
        contacInfo_lbl.setText("Contact Information")

        contact_lbl = QLabel("Contact no")
        self.contact_lne = QLineEdit()
        self.contact_lne.setFixedWidth(300)
        email_lbl = QLabel("Email")
        self.email_lne = QLineEdit()
        self.email_lne.setFixedWidth(300)

        self.displayPermissionText= QLabel("Display Permissions")
        self.displayPermissionText.setFont(QFont('Arial', 10))
        self.displayPermissionsTable_qwt = QTableWidget()
        self.displayPermissionsTable_qwt.setColumnCount(8)
        self.displayPermissionsTable_qwt.setHorizontalHeaderLabels(
            ['Username','CustomerScreen','PaymentScreen','AnalyticsScreen','SystemScreen','RoomsScreen','WaitlistScreen','ReportsScreen'])
        self.displayPermissionsTable_qwt.horizontalHeader().setStretchLastSection(True)
        rooms_lbl = QLabel("Rooms")
        self.rooms_qsb = QSpinBox()
        self.rooms_qsb.setFixedWidth(300)

        roomstype_label= QLabel("Rooms type")
        self.rooms_type = QComboBox()
        self.rooms_type.addItems(['','Conference','Business suite','Honey Moon suite','Standard suite'])
        self.rooms_type.setFixedWidth(300)
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setFixedWidth(100)

        form1.addRow(personalInfo)
        form1.addRow(name_lbl, self.name_lne)
        form1.addRow(surname_lbl,self.surname_lne)

        form1.addRow(address_lbl, self.address_lne)
        form1.addRow(self.gender_lbl)
        form1.addRow(self.male_qrb, self.female_qrb)
        form1.addRow(id_lbl, self.id_lne)
        form1.addRow(city_lbl, self.city_lne)
        form1.addRow(province_lbl, self.province_qcb)
        form1.setVerticalSpacing(20)
        form1.addRow(contacInfo_lbl)
        form1.addRow(contact_lbl, self.contact_lne)
        form1.addRow(email_lbl, self.email_lne)
        form1.addRow(self.clear_btn)

       # Second form layout
        form2 = QFormLayout()
        username_info = QLabel("Account Info")
        username_info.setFont(QFont('Arial',10))
        username_label = QLabel("Username:")

        self.username_lne = QLineEdit()
        checkin_label = QLabel("Password:")
        #checkout_label = QLabel("Check-out:")
        self.password_lne = QLineEdit()
        checkout_edit = QDateEdit()
        visit_category = QLabel()
        visit_category.setFont(QFont('Arial',10))
        visit_category.setText("User Type")

        self.admin_option1 =QRadioButton("Admin")
        self.viewer_option2 =QRadioButton("Viewer")
        self.editor_option3 = QRadioButton("Editor")

        self.deleteUserText_lbl = QLabel("Remove User")
        self.deleteUserText_lbl.setFont(QFont('Arial', 10))
        self.deleteUser_lne= QLineEdit()
        self.deleteUser_lne.setFixedWidth(300)
        self.deleteUser_lne.setPlaceholderText("type username")
        self.deletUser_btn = QPushButton("Delete User")
        self.deletUser_btn.setFixedWidth(100)
        self.deletUser_btn.clicked.connect(self.deleteUser)

        self.resetUserPassText_lbl = QLabel("Reset User Password")
        self.resetUserPassText_lbl.setFont(QFont('Arial', 10))
        self.resetUserPassText_lne=QLineEdit()
        self.resetUserPassText_lne.setPlaceholderText("type password")
        self.resetUserPassText_lne.setFixedWidth(300)
        self.resetUserPass_btn = QPushButton("Reset Password")
        self.resetUserPass_btn.setFixedWidth(100)
        self.resetUserPass_btn.clicked.connect(self.resetUserPassword)

        self.UsernamePassText_lne = QLineEdit()
        self.UsernamePassText_lne.setPlaceholderText("type username")
        self.UsernamePassText_lne.setFixedWidth(300)

        self.displayUsersTable_qwt = QTableWidget()
        self.displayUsersTable_qwt.setColumnCount(2)
        self.displayUsersTable_qwt.setHorizontalHeaderLabels(
            ['Username', 'Password'])
        self.displayUsersTable_qwt.horizontalHeader().setStretchLastSection(True)

        screenaccess_lbl = QLabel("Screen Access")
        screenaccess_lbl.setFont(QFont('Arial',10))

        # Screen Access
        self.customerScreen =QCheckBox("Customer Screen")
        self.paymentScreen = QCheckBox("Payment Screen")
        self.roomsScreen = QCheckBox("Room Screen")
        self.waitlistScreen = QCheckBox("Waitlist Screen")
        self.analyticsScreen = QCheckBox("Analytics Screen")
        self.reportsScreen = QCheckBox("Reports Screen")
        self.systemScreen = QCheckBox("System Screen")

        comments_label =QLabel("Comments")

        comments_box = QLineEdit()
        comments_box.setFixedHeight(200)
        create_button = QPushButton("Create")
        create_button.setFixedWidth(100)
        create_button.clicked.connect(self.createUser)
        form2.addRow(username_info)
        form2.addRow(username_label, self.username_lne)
        form2.addRow(checkin_label, self.password_lne)
        form2.setSpacing(20)
        form2.addRow(visit_category)
        form2.addRow(self.admin_option1,self.viewer_option2)
        form2.addRow(self.editor_option3)
        form2.addRow(screenaccess_lbl)
        form2.addRow(self.customerScreen,self.paymentScreen)
        form2.addRow(self.roomsScreen,self.waitlistScreen)
        form2.addRow(self.analyticsScreen,self.reportsScreen)
        form2.addRow(self.systemScreen)
        form2.addRow(create_button)

        form2.addRow(self.deleteUserText_lbl)
        form2.addRow(self.deleteUser_lne,self.deletUser_btn)
        form2.addRow(self.resetUserPassText_lbl)
        form2.addRow(self.displayUsersTable_qwt)
        form2.addRow(self.UsernamePassText_lne)
        form2.addRow(self.resetUserPassText_lne)
        form2.addRow(self.resetUserPass_btn)

        # Horizontal layout to hold both form layouts
        h_box = QHBoxLayout()
        h_box.addLayout(form1)
        h_box.addLayout(form2)

        # Tab 1 layout
        tab1_layout = QVBoxLayout()
        groupbox = QGroupBox("Details")
        groupbox.setLayout(h_box)
        tab1_layout.addWidget(groupbox)

        # Tab 2 layout
        self.searchEdit_lne = QLineEdit()
        self.searchEdit_lne.setFixedWidth(300)
        self.searchEdit_lne.setPlaceholderText("Enter name or ID")
        submitEdit_btn = QPushButton("Submit")
        submitEdit_btn.setFixedWidth(300)
        submitEdit_btn.clicked.connect(self.searchID)

        self.namePermission_lbl = QLabel("Name")
        self.namePermission_lne = QLineEdit()
        self.namePermission_lne.setFixedWidth(300)
        self.surnamePermission_lbl = QLabel("Surname")
        self.surnamePermission_lne = QLineEdit()
        self.surnamePermission_lne.setFixedWidth(300)
        self.addressPermission_lbl = QLabel("Address")
        self.addressPermission_lne = QLineEdit()
        self.addressPermission_lne.setFixedWidth(300)
        self.idPermission_lbl = QLabel("Id")
        self.idPermission_lne = QLineEdit()
        self.idPermission_lne.setFixedWidth(300)
        self.cityPermission_lbl = QLabel("City")
        self.cityPermission_lne = QLineEdit()
        self.cityPermission_lne.setFixedWidth(300)
        self.contactPermission_lbl = QLabel("Contact")
        self.contactPermission_lne = QLineEdit()
        self.contactPermission_lne.setFixedWidth(300)
        self.emailPermission_lbl = QLabel("Email")
        self.emailPermission_lne = QLineEdit()
        self.emailPermission_lne.setFixedWidth(300)
        daysEdit_lbl = QLabel("Day")
        daysEdit_lne = QLineEdit()
        daysEdit_lne.setFixedWidth(300)
        roomsEdit_lbl = QLabel("Rooms")
        roomsEdit_qsb = QSpinBox()
        roomsEdit_qsb.setFixedWidth(300)
        saveEdit_btn = QPushButton("save")
        saveEdit_btn.clicked.connect(self.updateDB)
        quitEdit_btn = QPushButton("quit")
        quitEdit_btn.setFixedWidth(300)

        tab2_layout =QVBoxLayout()
        form3 =QFormLayout()

        form3.addRow(self.searchEdit_lne, submitEdit_btn)
        form3.addRow(self.namePermission_lbl, self.namePermission_lne)
        form3.addRow(self.surnamePermission_lbl, self.surnamePermission_lne)
        form3.addRow(self.addressPermission_lbl, self.addressPermission_lne)
        form3.addRow(self.idPermission_lbl, self.idPermission_lne)
        form3.addRow(self.cityPermission_lbl, self.cityPermission_lne)
        form3.addRow(self.contactPermission_lbl, self.contactPermission_lne)
        form3.addRow(self.emailPermission_lbl, self.emailPermission_lne)
        form3.addRow(self.displayPermissionText)
        form3.addRow(self.displayPermissionsTable_qwt)
        form3.addRow(screenaccess_lbl)
        form3.addRow(self.customerScreen,self.roomsScreen)
        form3.addRow(self.paymentScreen,self.waitlistScreen)
        form3.addRow(self.analyticsScreen,self.reportsScreen)
        form3.addRow(self.systemScreen)
        form3.setVerticalSpacing(10)
        form3.addRow(saveEdit_btn, quitEdit_btn)

        groupboxEdit = QGroupBox("Edit")
        groupboxEdit.setLayout(form3)
        tab2_layout.addWidget(groupboxEdit)

        #Tab 3 layout
        searchAudit_lbl = QLabel("Search")
        self.searchAudit_lne = QLineEdit()
        self.searchAudit_lne.setFixedWidth(300)
        self.searchAudit_lne.setPlaceholderText("Enter username")
        submitAudit_btn = QPushButton("Get Permissions")
        submitAudit_btn.setFixedWidth(355)
        submitAudit_btn.clicked.connect(self.auditPermissions)
        tab3_layout = QVBoxLayout()
        form4 = QFormLayout()
        self.displayAuditTable_qwt=QTableWidget()
        self.displayAuditTable_qwt.setColumnCount(6)
        self.displayAuditTable_qwt.setHorizontalHeaderLabels(
            ['Timestamp', 'Username', 'Name', 'Role', 'Screen', 'Action'])
        self.displayAuditTable_qwt.horizontalHeader().setStretchLastSection(True)

        form4.addRow(searchAudit_lbl)
        form4.addRow(submitAudit_btn)
        form4.addRow(self.displayAuditTable_qwt)

        groupboxSearch4 = QGroupBox("Search")
        groupboxSearch4.setLayout(form4)
        tab3_layout.addWidget(groupboxSearch4)

        #tab layout 4
        tab4_layout = QVBoxLayout()

        #tab_layout5
        tab5_layout = QVBoxLayout()
        form6 = QFormLayout()
        backup_lbl = QLabel("Full database backup")

        backup_btn = QPushButton("Backup")
        backup_btn.setFixedWidth(355)
        backup_btn.clicked.connect(self.backupDB)
        tab5_layout = QVBoxLayout()

        form6 = QFormLayout()
        self.backupStatus_lbl = QLabel()
        self.backupStatus_lbl.setFixedWidth(800)
        form6.addRow(backup_lbl)

        form6.addRow(backup_btn)
        form6.addRow(self.backupStatus_lbl)

        groupboxSearch5 = QGroupBox("Menu")
        groupboxSearch5.setLayout(form6)
        tab5_layout.addWidget(groupboxSearch5)

        # tab_layout6
        tab6_layout = QVBoxLayout()
        form7 = QFormLayout()
        restore_lbl = QLabel("Path")
        self.restore_path_lbl = QLabel()
        self.restore_path_lbl.setFixedWidth(800)
        restore_btn =QPushButton("Restore")
        restore_btn.setFixedWidth(100)
        restore_btn.clicked.connect(self.restore_database)
        upload_btn = QPushButton("Upload")
        upload_btn.clicked.connect(self.upload_backup)

        tab6_layout = QVBoxLayout()
        form7 = QFormLayout()

        form7.addRow(restore_lbl, self.restore_path_lbl)
        form7.addRow(upload_btn,restore_btn)

        groupboxSearch7 = QGroupBox("Menu")
        groupboxSearch7.setLayout(form7)
        tab6_layout.addWidget(groupboxSearch7)

        # Tab widget
        tabs = QTabWidget()
        tabs.addTab(QWidget(), "Users")
        tabs.addTab(QWidget(), "Permissions")
        tabs.addTab(QWidget(), "Audit")
        tabs.addTab(QWidget(), "Backup")
        tabs.addTab(QWidget(), "Restore")

        tabs.widget(0).setLayout(tab1_layout)
        tabs.widget(1).setLayout(tab2_layout)
        tabs.widget(2).setLayout(tab3_layout)

        tabs.widget(3).setLayout(tab5_layout)
        tabs.widget(4).setLayout(tab6_layout)

        # Main layout
        main_layout = QFormLayout()
        main_layout.addRow(tabs)

        self.setLayout(main_layout)

        self.setWindowTitle("Customer Screen")
        self.setGeometry(100, 100, 1200, 900)
        self.setFixedSize(1200, 900)

        try:
            cnx = mysql.connector.connect(user='bee', password='P@ssword', host='localhost',
                                      auth_plugin='mysql_native_password', database='hmsdb')

            cursor3 = cnx.cursor()
            displayUsers_query = "SELECT username,passwords FROM users"
            cursor3.execute(displayUsers_query)
            result3 = cursor3.fetchall()
            print(result3)

            self.displayUsersTable_qwt.setRowCount(2)
            for row, item in enumerate(result3):
                self.displayUsersTable_qwt.insertRow(row)
                for col, value in enumerate(item):
                    table_item = QTableWidgetItem(str(value))

                    self.displayUsersTable_qwt.setItem(row, col, table_item)
                    print(row, col, item)

        except mysql.connector.Error as err:
            # Handle MySQL errors
            error_msg = f"MySQL Error: {err}"
            QMessageBox.critical(self, "Error", error_msg)
        except Exception as e:
            # Handle other exceptions
            error_msg = f"An error occurred: {e}"
            QMessageBox.critical(self, "Error", error_msg)
        finally:
            cursor3.close()
            cnx.close()

            print("Displayed Users")

    @pyqtSlot()
    def auditPermissions(self):
        try:
            print("Audit button clicked!!!")

            cnx = mysql.connector.connect(user='bee', password='P@ssword',
                                           host='localhost', auth_plugin='mysql_native_password', database='hmsdb')

            cursor4 = cnx.cursor()

            search_query4="SELECT timeaccess,username,nameofuser,accessrole,screenaccess,useraction FROM audit_log"

            cursor4.execute(search_query4)
            result4 = cursor4.fetchall()
            print("Data in Permissions Table: ", result4)

            self.displayAuditTable_qwt.setRowCount(6)
            for row, item in enumerate(result4):
                self.displayAuditTable_qwt.insertRow(row)
                for col, value in enumerate(item):
                    table_item = QTableWidgetItem(str(value))
                    self.displayAuditTable_qwt.setItem(row, col, table_item)
                    print(row, col, item)

        except mysql.connector.Error as err:
            # Handle MySQL errors
            error_msg = f"MySQL Error: {err}"
            QMessageBox.critical(self, "Error", error_msg)

        except Exception as e:
            # Handle other exceptions
            error_msg = f"An error occurred: {e}"
            QMessageBox.critical(self, "Error", error_msg)
        finally:
            cursor4.close()
            cnx.close()

    def getRoles(self):
        if self.admin_option1.isChecked():
            self.admin_option1.setChecked(True)
            self.roles= "Admin"

        if self.viewer_option2.isChecked():
            self.viewer_option2.setChecked(True)
            self.roles= "Viewer"

        if self.editor_option3.isChecked():
            self.editor_option3.setChecked(True)
            self.roles ="Editor"

        return self.roles

    @pyqtSlot()
    def createUser(self):
        try:
            # Get the values from UI components here
            cnx = mysql.connector.connect(user='bee', password='P@ssword', host='localhost',
                                          auth_plugin='mysql_native_password', database='hmsdb')
            cursor = cnx.cursor()

            sql = """
                            INSERT INTO users (username, email, passwords, nameofuser,surnameofuser,address,gender, id_number, city, province, contact, userroles)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

                                        """
            values = (self.username_lne.text(),self.email_lne.text(),self.password_lne.text(),self.name_lne.text(), self.surname_lne.text(), self.address_lne.text(),
                      self.gender, self.id_lne.text(),self.city_lne.text(), self.province_qcb.currentText(),self.contact_lne.text(),self.getRoles())

            cursor.execute(sql, values)
            print(values)
            cnx.commit()

            cursor = cnx.cursor()
            perm_query="INSERT INTO acl (users_username) VALUES (%s)"
            perm_uname= self.username_lne.text()
            cursor.execute(perm_query,(perm_uname,))
            cnx.commit()

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
            QMessageBox.warning(self, 'Info', 'Inserted Succesfully.')
            #print("Generated SQL query:", sql % values)
            print("Data inserted")

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
            search_query = "SELECT nameofuser,surnameofuser,address, id_number, city, contact,email FROM users WHERE username = %s"
            # cursor.execute(query,self.search_lne.text())
            cursor.execute(search_query, (search_term,))
            result = cursor.fetchall()
            print('Data in Users Table',result)

            for items in result:
                print(items[0])
                name=items[0]
                surname=items[1]
                address=items[2]
                id=items[3]
                city=items[4]
                contact=items[5]
                email=items[6]
                self.namePermission_lne.setText(str(name))
                self.surnamePermission_lne.setText(str(surname))
                self.addressPermission_lne.setText(str(address))
                self.idPermission_lne.setText(str(id))
                self.cityPermission_lne.setText(str(city))
                self.contactPermission_lne.setText(str(contact))
                self.emailPermission_lne.setText(str(email))

            cursor2 = cnx.cursor()
            search_query2 = "SELECT users_username,customerscreen,paymentscreen,analyticsscreen,systemsscreen,roomscreen,waitlistscreen,reportsscreen FROM acl WHERE users_username =%s"
            cursor2.execute(search_query2, (search_term,))
            result2 = cursor2.fetchall()
            print("Data in Permissions Table: ", result2)

            self.displayPermissionsTable_qwt.setRowCount(len(result2))

            for row_idx, row in enumerate(result2):
                for col_idx, value in enumerate(row):
                    table_item = QTableWidgetItem(str(value))
                    self.displayPermissionsTable_qwt.setItem(row_idx, col_idx, table_item)
                    print(row_idx,col_idx,table_item,value)

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

    @pyqtSlot()
    def editToDB(self):
        try:
            print("getdata button clicked!!!")
            search_term = self.searchEdit_lne.text()
            print(search_term)
            cnx = mysql.connector.connect(user='bee', password='P@ssword',
                                          host='localhost', auth_plugin='mysql_native_password', database='hmsdb')
            cursor = cnx.cursor()
            # Check if username and password exist in database

            search_query = "UPDATE Customers SET first_name=%s, last_name=%s, address=%s, id_number=%s, city=%s, phone=%s, email=%s WHERE id_number = %s"

            cnx.commit()
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
    def updateDB(self):
        print("Saved Button Clicked!!!")
        try:
            print("getdata button clicked!!!")
            search_term = self.searchEdit_lne.text()
            print(search_term)
            cnx = mysql.connector.connect(user='bee', password='P@ssword',
                                          host='localhost', auth_plugin='mysql_native_password', database='hmsdb')

            name = self.namePermission_lne.text()
            print("Permission name:",name)
            surname = self.surnamePermission_lne.text()
            address = self.addressPermission_lne.text()
            id = self.idPermission_lne.text()
            city = self.cityPermission_lne.text()
            contact = self.contactPermission_lne.text()
            email = self.emailPermission_lne.text()

            # Check if username and password exist in database
            cursor = cnx.cursor()
            search_query = "UPDATE users SET nameofuser= %s,surnameofuser=%s,address=%s, id_number=%s, city=%s, contact=%s,email=%s WHERE username = %s"
            cursor.execute(search_query, (name, surname, address, id, city, contact, email, search_term))
            cnx.commit()

            if self.customerScreen.isChecked():
                self.yes_customerscreen = 'yes'
                print("Customer Screen permission=", self.yes_customerscreen)
                yes_cust_query="UPDATE acl SET customerscreen = %s WHERE users_username=%s"
                cursor.execute(yes_cust_query, (self.yes_customerscreen,search_term))
                cnx.commit()
            else:
                self.no_customerscreen ='no'
                no_cust_query = "UPDATE acl SET customerscreen = %s WHERE users_username=%s"
                cursor.execute(no_cust_query, (self.no_customerscreen, search_term))
                cnx.commit()
                print("Customer Screen permission=", self.no_customerscreen)

            if self.paymentScreen.isChecked():
                self.yes_paymentscreen = 'yes'
                print("Payments Screen permission=", self.yes_customerscreen)
                yes_pay_query="UPDATE acl SET paymentscreen = %s WHERE users_username=%s"
                cursor.execute(yes_pay_query, (self.yes_paymentscreen,search_term))
                cnx.commit()
            else:
                self.no_paymentscreen ='no'
                no_pay_query = "UPDATE acl SET paymentscreen = %s WHERE users_username=%s"
                cursor.execute(no_pay_query, (self.no_paymentscreen, search_term))
                cnx.commit()
                print("Analytics Screen permission=", self.no_paymentscreen)

            if self.analyticsScreen.isChecked():
                self.yes_analyticsscreen = 'yes'
                print("Analytics Screen permission=", self.yes_customerscreen)
                yes_anal_query="UPDATE acl SET analyticsscreen = %s WHERE users_username=%s"
                cursor.execute(yes_anal_query, (self.yes_analyticsscreen,search_term))
                cnx.commit()
            else:
                self.no_analyticsscreen ='no'
                no_anal_query = "UPDATE acl SET analyticsscreen = %s WHERE users_username=%s"
                cursor.execute(no_anal_query, (self.no_analyticsscreen, search_term))
                cnx.commit()
                print("Analytics Screen permission=", self.no_analyticsscreen)

            if self.systemScreen.isChecked():
                self.yes_systemsscreen = 'yes'
                print("Systems Screen permission=", self.yes_systemsscreen)
                yes_sys_query="UPDATE acl SET systemsscreen = %s WHERE users_username=%s"
                cursor.execute(yes_sys_query, (self.yes_systemsscreen,search_term))
                cnx.commit()
            else:
                self.no_systemsscreen ='no'
                no_sys_query = "UPDATE acl SET systemsscreen = %s WHERE users_username=%s"
                cursor.execute(no_sys_query, (self.no_systemsscreen, search_term))
                cnx.commit()
                print("Systems Screen permission=", self.no_systemsscreen)

            if self.roomsScreen.isChecked():
                self.yes_roomscreen = 'yes'
                print("Room Screen permission=", self.yes_roomscreen)
                yes_ro_query="UPDATE acl SET roomscreen = %s WHERE users_username=%s"
                cursor.execute(yes_ro_query, (self.yes_roomscreen,search_term))
                cnx.commit()
            else:
                self.no_roomscreen ='no'
                no_ro_query = "UPDATE acl SET roomscreen = %s WHERE users_username=%s"
                cursor.execute(no_ro_query, (self.no_roomscreen, search_term))
                cnx.commit()
                print("Room Screen permission=", self.no_roomscreen)

            if self.waitlistScreen.isChecked():
                self.yes_waitlistscreen = 'yes'
                print("Waitlist Screen permission=", self.yes_waitlistscreen)
                yes_wa_query="UPDATE acl SET waitlistscreen = %s WHERE users_username=%s"
                cursor.execute(yes_wa_query, (self.yes_waitlistscreen,search_term))
                cnx.commit()
            else:
                self.no_waitlistscreen ='no'
                no_wa_query = "UPDATE acl SET waitlistscreen = %s WHERE users_username=%s"
                cursor.execute(no_wa_query, (self.no_waitlistscreen, search_term))
                cnx.commit()
                print("Waitlist Screen permission=", self.no_waitlistscreen)

            if self.reportsScreen.isChecked():
                self.yes_reportsscreen = 'yes'
                print("Reports Screen permission=", self.yes_reportsscreen)
                yes_rep_query="UPDATE acl SET reportsscreen = %s WHERE users_username=%s"
                cursor.execute(yes_rep_query, (self.yes_reportsscreen,search_term))
                cnx.commit()
            else:
                self.no_reportsscreen ='no'
                no_rep_query = "UPDATE acl SET reportsscreen = %s WHERE users_username=%s"
                cursor.execute(no_rep_query, (self.no_reportsscreen, search_term))
                cnx.commit()
                print("Reports Screen permission=", self.no_reportsscreen)

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
            QMessageBox.warning(self, 'Info', 'Updated Succesfully.')
            print("Generated SQL query:")

    @pyqtSlot()
    def deleteUser(self):
        try:
            print("delete button clicked!!!")
            search_term = self.deleteUser_lne.text()
            print(search_term)
            cnx = mysql.connector.connect(user='bee', password='P@ssword',
                                          host='localhost', auth_plugin='mysql_native_password', database='hmsdb')

            # Check if username and password exist in database
            cursor = cnx.cursor()
            deletePerm_query = "DELETE FROM ACL WHERE users_username = %s"
            cursor.execute(deletePerm_query, (search_term,))
            cnx.commit()

            deleteUser_query ="DELETE FROM USERS WHERE username = %s"
            cursor.execute(deleteUser_query, (search_term,))
            cnx.commit()

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
            QMessageBox.warning(self, 'Info', 'Deleted Succesfully.')
            print("Generated SQL query:")
    @pyqtSlot()
    def resetUserPassword(self):
        try:
            print("reset password button clicked!!!")
            search_term = self.resetUserPassText_lne.text()
            username= self.UsernamePassText_lne.text()
            print(search_term)
            cnx = mysql.connector.connect(user='bee', password='P@ssword',
                                          host='localhost', auth_plugin='mysql_native_password', database='hmsdb')

            # Check if username and password exist in database
            cursor = cnx.cursor()
            updatePasswords_query = "UPDATE users SET passwords = %s WHERE username = %s"
            cursor.execute(updatePasswords_query, (search_term,username))
            cnx.commit()

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
            QMessageBox.warning(self, 'Info', 'Reset Succesfully.')
            print("Generated SQL query:")
    def updateStatus(self, message):
        self.backupStatus_lbl .setText(message)
    @pyqtSlot()
    def backupDB(self):
        print("Backup button clicked")

        # Set your MySQL connection details
        host = "localhost"
        user = "bee"
        password = "P@ssword"
        database = "hmsdb"
        auth_plugin = "mysql_native_password"

        try:
            # Create a connection to the database
            cnx = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                auth_plugin=auth_plugin
            )

            # Specify the full path to the mysqldump executable
            mysqldump_path = r"C:\Program Files\MySQL\MySQL Workbench 8.0 CE\mysqldump.exe"

            # Generate a timestamp to include in the filename
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            # Construct the backup filename with a timestamp
            backup_filename = f"backup_{timestamp}.sql"

            # Specify the path where you want to save the backup file
            backup_file_path = r"C:\users\brendon"  # Adjust the directory as needed
            backup_file_path = backup_file_path + "\\" + backup_filename

            # Start a thread to execute the backup command
            backup_thread = threading.Thread(
                target=self.run_backup,
                args=(mysqldump_path, host, user, password, database, backup_file_path)
            )
            backup_thread.start()
        except Exception as e:
            self.updateStatus(f"Backup failed. Error: {str(e)}")
        finally:
            # Close the connection
            cnx.close()

    def run_backup(self, mysqldump_path, host, user, password, database, backup_file_path):
        try:
            # Execute the backup command and capture output
            process = subprocess.Popen(
                [
                    mysqldump_path,
                    f"--host={host}",
                    f"--user={user}",
                    f"--password={password}",
                    database
                ],
                stdout=open(backup_file_path, "w"),
                stderr=subprocess.PIPE,
                text=True
            )
            # Wait for the process to complete
            process.communicate()

            if process.returncode == 0:
                self.updateStatus(f"Backup completed successfully. Filename: {backup_file_path}")
            else:
                self.updateStatus(f"Backup failed. Error: {process.stderr}")
        except Exception as e:
            self.updateStatus(f"An error occurred: {str(e)}")

    def upload_backup(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select Backup File', '', 'SQL Files (*.sql);;All Files (*)')

        if file_path:
            self.backup_path = file_path
            self.restore_path_lbl.setText(f'Backup Path: {self.backup_path}')

    def restore_database(self):
        print("Restore button clickec")
        if hasattr(self, 'backup_path'):

            mysql_cmd = f'mysql -u your_mysql_username -p your_mysql_password your_database_name < {self.backup_path}'

            try:
                subprocess.run(mysql_cmd, shell=True, check=True)
                print("Database restored successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error restoring database: {e}")
        else:
            print("Please upload a database backup first.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = systemmenu()
    form.show()
    sys.exit(app.exec_())
