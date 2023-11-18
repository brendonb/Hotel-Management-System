import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QFormLayout, QLineEdit,
                             QLabel, QPushButton, QHBoxLayout, QTabWidget, QVBoxLayout, QGroupBox,
                             QRadioButton, QSpinBox, QComboBox, QDateEdit, QTableWidget, QMessageBox, QTableWidgetItem,
                             QButtonGroup)

from PyQt5.QtCore import pyqtSlot

from PyQt5.QtGui import QFont
import mysql
import mysql.connector
from mysql.connector import connect, Error
from self import self


class Customers(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(400, 300)

        # First form layout
        form1 = QFormLayout()

        personalInfo = QLabel()
        personalInfo.setFont(QFont('Arial',10))
        personalInfo.setText("Personal Info")

        self.name_lne = QLineEdit(self)
        self.name_lne.setFixedWidth(300)
        name_lbl = QLabel("Name")
        self.name = self.name_lne.text()

        surname_lbl = QLabel("Surname")
        self.surname_lne = QLineEdit(self)
        self.surname_lne.setFixedWidth(300)
        self.surname = self.surname_lne.text()

        address_lbl = QLabel("Address")
        self.address_lne = QLineEdit(self)
        self.address_lne.setFixedSize(300,100)
        self.address= self.address_lne.text()

        gender_lbl = QLabel("Gender")
        self.gender_qcb = QComboBox(self)
        self.gender_qcb.addItems(['', 'Male', 'Female'])
        self.gender = self.gender_qcb.currentText()
        self.gender_qcb.setFixedWidth(300)

        id_lbl = QLabel("ID no")
        self.id_lne = QLineEdit(self)
        self.id_lne.setFixedWidth(300)
        self.id = self.id_lne.text()

        city_lbl = QLabel("City")
        self.city_lne = QLineEdit(self)
        self.city_lne.setFixedWidth(300)
        self.city= self.city_lne.text()


        province_lbl = QLabel("Province")
        self.province_qcb = QComboBox(self)
        self.province_qcb.addItems(['', 'Western Cape', 'Eastern Cape', 'Northen Cape', 'Southern Cape',
                                    'Gauteng'])
        self.province =self.province_qcb.currentText()

        self.province_qcb.setFixedWidth(300)
        contacInfo_lbl = QLabel()
        contacInfo_lbl.setFont(QFont('Arial', 10))
        contacInfo_lbl.setText("Contact Information")

        contact_lbl = QLabel("Contact no")
        self.contact_lne = QLineEdit(self)
        self.contact_lne.setFixedWidth(300)
        self.contact= self.contact_lne.text()

        email_lbl = QLabel("Email")
        self.email_lne = QLineEdit(self)
        self.email_lne.setFixedWidth(300)
        self.email= self.email_lne.text()

        rooms_lbl = QLabel("Rooms ID")
        self.rooms_qsb = QLineEdit(self)
        self.rooms_qsb.setFixedWidth(300)
        #rooms=rooms_qsb.value()

        roomstype_label= QLabel("Rooms type")
        self.rooms_type = QComboBox(self)
        self.rooms_type.addItems(['','Conference','Business suite','Honey Moon suite','Standard suite'])
        self.rooms_type.setFixedWidth(300)
        self.roomstype =self.rooms_type.currentText()

        clear_btn = QPushButton("Clear")
        clear_btn.setFixedWidth(100)

        form1.addRow(personalInfo)
        form1.addRow(name_lbl, self.name_lne)
        form1.addRow(surname_lbl,self.surname_lne)

        form1.addRow(address_lbl, self.address_lne)
        form1.addRow(gender_lbl,self.gender_qcb)
        form1.addRow(id_lbl, self.id_lne)
        form1.addRow(city_lbl, self.city_lne)
        form1.addRow(province_lbl, self.province_qcb)
        form1.setVerticalSpacing(20)
        form1.addRow(contacInfo_lbl)
        form1.addRow(contact_lbl, self.contact_lne)
        form1.addRow(email_lbl,self.email_lne)

        form1.addRow(rooms_lbl, self.rooms_qsb)
        form1.addRow(roomstype_label,self.rooms_type)
        form1.addRow(clear_btn)

       # Second form layout
        form2 = QFormLayout()
        date_label = QLabel("Date:")

        date_edit = QLineEdit()
        checkin_label = QLabel("Check-in:")
        checkout_label = QLabel("Check-out:")

        checkin_edit = QDateEdit()
        checkin_date =checkin_edit.date().toPyDate()
        checkout_edit = QDateEdit()
        checkout_date =checkout_edit.date().toPyDate()

        visit_category = QLabel()
        visit_category.setFont(QFont('Arial',10))
        visit_category.setText("Visite Type")

        waitlist_lbl = QLabel("Waitlist")
        self.waitlist_qcb = QComboBox(self)
        self.waitlist_qcb.addItems(['', 'Yes', 'No'])
        self.waitlist = self.waitlist_qcb.currentText()

        self.waitlist_qcb.setFixedWidth(300)


        visit_option1 =QRadioButton("Business")
        visit_option2 =QRadioButton("Holiday")
        visitoption ="Business" if visit_option1.isChecked() else "Holiday"

        comments_label =QLabel("Comments")

        self.comments_box = QLineEdit(self)
        self.comments_box.setFixedHeight(200)
        self.comments = self.comments_box.text()

        submit_button = QPushButton("Submit")
        submit_button.setFixedWidth(100)
        submit_button.clicked.connect(self.saveToDB)

        form2.addRow(date_label, date_edit)
        form2.addRow(checkin_label, checkin_edit)
        form2.addRow(checkout_label,checkout_edit)
        form2.setSpacing(20)
        form2.addRow(visit_category)
        form2.addRow(visit_option1,visit_option2)

        #wait list qcb
        form2.addRow(waitlist_lbl)
        form2.addRow(self.waitlist_qcb)

        form2.addRow(comments_label)
        form2.addRow(self.comments_box)
        form2.addRow(submit_button)

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
        submitEdit_btn.clicked.connect(self.displayEditCust)

        nameEdit_lbl = QLabel("Name")
        self.nameEdit_lne = QLineEdit()
        self.nameEdit_lne.setFixedWidth(300)
        self.surnameEdit_lbl = QLabel("Surname")
        self.surnameEdit_lne = QLineEdit()
        self.surnameEdit_lne.setFixedWidth(300)
        self.addressEdit_lbl = QLabel("Address")
        self.addressEdit_lne = QLineEdit()
        self.addressEdit_lne.setFixedWidth(300)
        self.idEdit_lbl = QLabel("Id")
        self.idEdit_lne = QLineEdit()
        self.idEdit_lne.setFixedWidth(300)
        self.cityEdit_lbl = QLabel("City")
        self.cityEdit_lne = QLineEdit()
        self.cityEdit_lne.setFixedWidth(300)
        self.contactEdit_lbl = QLabel("Contact")
        self.contactEdit_lne = QLineEdit()
        self.contactEdit_lne.setFixedWidth(300)
        self.emailEdit_lbl = QLabel("Email")
        self.emailEdit_lne = QLineEdit()
        self.emailEdit_lne.setFixedWidth(300)
        saveEdit_btn = QPushButton("save")
        saveEdit_btn.clicked.connect(self.editToDB)
        quitEdit_btn = QPushButton("quit")
        quitEdit_btn.setFixedWidth(300)

        tab2_layout =QVBoxLayout()
        form3 =QFormLayout()

        form3.addRow(self.searchEdit_lne, submitEdit_btn)
        form3.addRow(nameEdit_lbl, self.nameEdit_lne)
        form3.addRow(self.surnameEdit_lbl, self.surnameEdit_lne)
        form3.addRow(self.addressEdit_lbl, self.addressEdit_lne)
        form3.addRow(self.idEdit_lbl, self.idEdit_lne)
        form3.addRow(self.cityEdit_lbl, self.cityEdit_lne)
        form3.addRow(self.contactEdit_lbl, self.contactEdit_lne)
        form3.addRow(self.emailEdit_lbl, self.emailEdit_lne)
        form3.setVerticalSpacing(10)
        form3.addRow(saveEdit_btn, quitEdit_btn)

        groupboxEdit = QGroupBox("Edit")
        groupboxEdit.setLayout(form3)
        tab2_layout.addWidget(groupboxEdit)


        # Tab 3 layout
        search_lbl = QLabel("Search")
        self.search_lne = QLineEdit()
        self.search_lne.setFixedWidth(300)
        displayData_btn = QPushButton("Display")
        displayData_btn.setFixedWidth(355)
        displayData_btn.clicked.connect(self.getData)
        searchData_btn = QPushButton("Search")
        searchData_btn.setFixedWidth(355)
        searchData_btn.clicked.connect(self.searchID)


        tab3_layout = QVBoxLayout()
        form4 = QFormLayout()
        self.displayPayments_qwt=QTableWidget()
        self.displayPayments_qwt.setColumnCount(16)
        self.displayPayments_qwt.setHorizontalHeaderLabels(['Name', 'Surname', 'Address', 'Gender', 'Id_number', 'City', 'Province', 'Phone', 'Email', 'Check_in', 'Check_out', 'Visite_type', 'Comments', 'Room_number', 'Room_type', 'Waitlist'])
        self.displayPayments_qwt.horizontalHeader().setStretchLastSection(True)


        form4.addRow(displayData_btn)
        form4.addRow(self.displayPayments_qwt)
        form4.addRow(searchData_btn, self.search_lne)

        groupboxSearch = QGroupBox("Search")
        groupboxSearch.setLayout(form4)
        tab3_layout.addWidget(groupboxSearch)

        # Tab widget
        tabs = QTabWidget()
        tabs.addTab(QWidget(), "Add Customers")
        tabs.addTab(QWidget(), "Edit Customer")
        tabs.addTab(QWidget(),"Search Customer")

        tabs.widget(0).setLayout(tab1_layout)
        tabs.widget(1).setLayout(tab2_layout)
        tabs.widget(2).setLayout(tab3_layout)

        # Main layout
        main_layout = QFormLayout()
        main_layout.addRow(tabs)

        self.setLayout(main_layout)

        self.setWindowTitle("Customer Screen")
        self.setGeometry(100, 100, 1200, 900)
        self.setFixedSize(1200, 900)

        self.check_in = checkin_edit.date().toString("yyyy-MM-dd")
        self.check_out = checkout_edit.date().toString("yyyy-MM-dd")
        self.visite_type = "Business" if visit_option1.isChecked() else "Holiday"

    @pyqtSlot()
    def saveToDB(self):
        try:
            # Get the values from UI components here
            self.first_name = self.name_lne.text()

            cnx = mysql.connector.connect(user='bee', password='P@ssword', host='localhost',
                                          auth_plugin='mysql_native_password', database='hmsdb')
            cursor = cnx.cursor()

            sql = """
                            INSERT INTO customers (first_name, last_name, address, gender, id_number, city, province, email, phone,
                                                check_in, check_out, visite_type, comments, room_number, room_type, waitlist)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    """
            values = (self.name_lne.text(), self.surname_lne.text(), self.address_lne.text(), self.gender_qcb.currentText(), self.id_lne.text(), self.city_lne.text(), self.province_qcb.currentText(),
                      self.email_lne.text(), self.contact_lne.text(), self.check_in, self.check_out, self.visite_type, self.comments_box.text(),
                       self.rooms_qsb.text(),self.rooms_type.currentText(),self.waitlist_qcb.currentText())
            #print(self.gender)
            cursor.execute(sql, values)
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

            print("Generated SQL query:", sql % values)
            print("Data inserted")

    @pyqtSlot()
    def getData(self):
        print('Get Data Clicked!!!')
        try:
            print("getdata button clicked!!!")
            search_term=self.search_lne.text()
            print(search_term)
            cnx = mysql.connector.connect(user='bee', password='P@ssword',
                                      host='localhost', auth_plugin='mysql_native_password', database='hmsdb')
            cursor = cnx.cursor()

            # Check if username and password exist in database

            search_query = "SELECT first_name, last_name, address, gender, id_number, city, province, phone,  email, check_in, check_out, visite_type, comments, room_number, room_type,waitlist FROM customers"

            cursor.execute(search_query)
            result = cursor.fetchall()
            print(result)
            self.displayPayments_qwt.setRowCount(len(result))

            for row_idx, row in enumerate(result):
                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value))

                    self.displayPayments_qwt.setItem(row_idx, col_idx, item)
                    print(row_idx,col_idx,item,value)

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
            print("Generated SQL query:", search_query )

        # Close database connection
    @pyqtSlot()
    def searchID(self):
        print("search id clicked")
        try:
            print("search id button clicked!!!")
            search_term=self.search_lne.text()
            print(search_term)
            cnx = mysql.connector.connect(user='bee', password='P@ssword',
                                      host='localhost', auth_plugin='mysql_native_password', database='hmsdb')
            cursor = cnx.cursor()

            search_query = "SELECT first_name, last_name, address, gender, id_number, city, province, phone, email, check_in, check_out, visite_type, comments, room_number, room_type FROM customers WHERE cust_id = %s"

            cursor.execute(search_query,(search_term,))
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
            #Handle MySQL errors
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
    def displayEditCust(self):
        try:
            print("getdata button clicked!!!")
            search_term=self.searchEdit_lne.text()
            print(search_term)
            cnx = mysql.connector.connect(user='bee', password='P@ssword',
                                      host='localhost', auth_plugin='mysql_native_password', database='hmsdb')
            cursor = cnx.cursor()

            # Check if username and password exist in database

            search_query = "SELECT first_name,last_name,address,id_number,city,phone,email FROM customers WHERE id_number= %s"
            #cursor.execute(query,self.search_lne.text())
            cursor.execute(search_query,(search_term,))
            result = cursor.fetchone()
            print(result)

            if result:
                self.nameEdit_lne.setText(result[0])
                self.surnameEdit_lne.setText(result[1])
                self.addressEdit_lne.setText(result[2])
                self.idEdit_lne.setText(result[3])
                self.cityEdit_lne.setText(result[4])
                self.contactEdit_lne.setText(result[5])
                self.emailEdit_lne.setText(result[6])
            else:
                print("error")

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
            print("Generated SQL query:", search_query )

        # Close database connection

    @pyqtSlot()
    def editToDB(self):
        try:
            print("getdata button clicked!!!")
            search_term=self.searchEdit_lne.text()
            print(search_term)
            cnx = mysql.connector.connect(user='bee', password='P@ssword',
                                      host='localhost', auth_plugin='mysql_native_password', database='hmsdb')
            cursor = cnx.cursor()

            name=self.nameEdit_lne.text()
            surname=self.surnameEdit_lne.text()
            address=self.addressEdit_lne.text()
            id=self.idEdit_lne.text()
            city=self.cityEdit_lne.text()
            contact=self.contactEdit_lne.text()
            email=self.emailEdit_lne.text()

            # Check if username and password exist in database

            search_query = "UPDATE Customers SET first_name=%s, last_name=%s, address=%s, id_number=%s, city=%s, phone=%s, email=%s WHERE id_number = %s"
            #cursor.execute(query,self.search_lne.text())
            cursor.execute(search_query,(name,surname,address,id,city,contact,email,search_term))
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
            print("Generated SQL query:", search_query )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Customers()
    form.show()
    sys.exit(app.exec_())


