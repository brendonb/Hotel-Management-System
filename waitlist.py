import os,sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QLineEdit, QPushButton, QTableWidget,
                             QFrame, QFormLayout, QGroupBox, QVBoxLayout, QTableWidgetItem, QMessageBox)
import mysql
import mysql.connector

class waitlist(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        form = QFormLayout()

        # variables
        self.searchRooms_lne = QLineEdit()
        self.searchRooms_lne.setPlaceholderText("Enter room type")
        self.searchRooms_lne.setFixedWidth(300)

        waitlist_btn = QPushButton("Display")
        waitlist_btn.setFixedWidth(300)
        waitlist_btn.clicked.connect(self.getData)

        roomsItems_btn = QPushButton("Search")
        roomsItems_btn.setFixedWidth(300)
        roomsItems_btn.clicked.connect(self.searchID)

        quit_btn = QPushButton("Quit")
        quit_btn.setFixedWidth(300)

        qvb_layout = QVBoxLayout()

        self.displayWaitlistTable_qwt = QTableWidget()
        self.displayWaitlistTable_qwt.setColumnCount(6)
        self.displayWaitlistTable_qwt.setHorizontalHeaderLabels(
            ['Name', 'Surname', 'ID number','Email','Phone','Waitlist' ])
        self.displayWaitlistTable_qwt.horizontalHeader().setStretchLastSection(True)

        form.addRow(waitlist_btn)
        form.addRow(self.displayWaitlistTable_qwt)
        form.addRow(roomsItems_btn, self.searchRooms_lne)
        room_qgb = QGroupBox("Available rooms")
        room_qgb.setLayout(form)
        qvb_layout.addWidget(room_qgb)
        self.setLayout(qvb_layout)

        self.setWindowTitle("Rooms screen")
        self.setGeometry(100, 100, 1200, 900)
        self.setFixedSize(1200, 900)

    @pyqtSlot()
    def getData(self):
        print('Get Data Clicked!!!')
        try:
            print("getdata button clicked!!!")

            cnx = mysql.connector.connect(user='bee', password='P@ssword',
                                          host='localhost', auth_plugin='mysql_native_password', database='hmsdb')
            cursor = cnx.cursor()



            search_query = "SELECT first_name, last_name, id_number,email,phone,waitlist FROM customers;"

            cursor.execute(search_query)
            result = cursor.fetchall()
            print(result)
            self.displayWaitlistTable_qwt.setRowCount(len(result))

            for row_idx, row in enumerate(result):
                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value))

                    self.displayWaitlistTable_qwt.setItem(row_idx, col_idx, item)
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
            search_term = self.searchRooms_lne.text()
            print(search_term)
            cnx = mysql.connector.connect(user='bee', password='P@ssword',
                                          host='localhost', auth_plugin='mysql_native_password', database='hmsdb')
            cursor = cnx.cursor()

            search_query = "SELECT first_name, last_name, id_number,email,phone,waitlist  FROM Customers WHERE cust_id = %s"

            cursor.execute(search_query, (search_term,))
            result = cursor.fetchall()
            print(result)
            self.displayWaitlistTable_qwt.setRowCount(len(result))

            for row_idx, row in enumerate(result):
                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value))

                    self.displayWaitlistTable_qwt.setItem(row_idx, col_idx, item)
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
    app =QApplication(sys.argv)
    window =waitlist()
    window.show()
    sys.exit(app.exec_())