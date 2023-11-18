import csv
import os,sys
import subprocess
from reportlab.pdfgen import canvas
import mysql
import mysql.connector
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QLineEdit, QPushButton, QFormLayout,
                             QRadioButton, QComboBox, QSpinBox, QDateEdit, QVBoxLayout, QHBoxLayout, QGroupBox,
                             QTableWidget, QTabWidget, QMessageBox, QTableWidgetItem)
from pyqtgraph import PlotWidget, plot
from PyQt5.QtGui import QFont
import pyqtgraph as pg
from PyQt5.QtCore import pyqtSlot
from reportlab.pdfgen import canvas


class reports(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
            self.resize(400, 300)

            # First form layout
            form1 = QFormLayout()
            self.displayContent = QTableWidget()
            self.displayContent.setColumnCount(5)
            self.displayContent.setHorizontalHeaderLabels(
                    ['Name', 'Surname', 'Username', 'Creation Time','Role'])

            printBtnUser= QPushButton("Print PDF")

            printBtnUser.clicked.connect(self.export_to_pdf)
            printBtnUser.setFixedWidth(100)
            printBtnUserCsv = QPushButton("Print CSV")
            printBtnUserCsv.setFixedWidth(100)
            printBtnUserCsv.clicked.connect(self.export_to_csv)
            form1.addRow(self.displayContent)
            form1.addRow(printBtnUser,printBtnUserCsv)

            # Second form layout
            form2 = QFormLayout()
            printBtnFinance = QPushButton("Print PDF")
            printBtnFinance.setFixedWidth(100)
            printBtnFinance.clicked.connect(self.export_to_pdf)
            printBtnFinanceCsv = QPushButton("Print CSV")
            printBtnFinanceCsv.setFixedWidth(100)
            printBtnFinanceCsv.clicked.connect(self.export_to_csv)

            self.displayContentFinance = QTableWidget()
            self.displayContentFinance.setColumnCount(7)
            self.displayContentFinance.setHorizontalHeaderLabels(
                    ['Name', 'Surname', 'Email', 'Phone', 'Card_type','Card_no','Amount'])
            printBtnFinance.setFixedWidth(100)

            form2.addRow(self.displayContentFinance)

            form2.addRow(printBtnFinance,printBtnFinanceCsv)
            # Third form layout
            form3 = QFormLayout()
            printBtncustomer = QPushButton("Print")
            printBtncustomer = QPushButton("Print PDF")
            printBtncustomer.setFixedWidth(100)
            printBtncustomer.clicked.connect(self.export_to_pdf)

            printBtncustomerCsv = QPushButton("Print CSV")
            printBtncustomerCsv.setFixedWidth(100)

            printBtncustomer.setFixedWidth(100)
            printBtncustomer.clicked.connect(self.export_to_csv)

            displayContentFinance = QTableWidget()


            self.displayContentCustomer = QTableWidget()
            self.displayContentCustomer.setColumnCount(5)
            self.displayContentCustomer.setHorizontalHeaderLabels(
                    ['Name', 'Surname', 'City', 'Province', 'Visit type'])
            self.displayContentCustomer.setFixedWidth(650)
            form3.addRow(self.displayContentCustomer)
            form3.addRow(printBtncustomer,printBtncustomerCsv)

            # Main layout
            groupbox1 = QGroupBox("User reporting")
            groupbox1.setLayout(form1)
            groupbox2 = QGroupBox("Financial reporting")
            groupbox2.setLayout(form2)
            groupbox3 = QGroupBox("Customer reporting")
            groupbox3.setLayout(form3)

            hbox_layout = QHBoxLayout()
            hbox_layout.addLayout(form1)
            hbox_layout.addLayout(form2)

            top_layout = QHBoxLayout()
            top_layout.addWidget(groupbox1)
            top_layout.addWidget(groupbox2)

            bottom_layout = QVBoxLayout()
            bottom_layout.addWidget(groupbox3)

            main_layout = QVBoxLayout()
            main_layout.addLayout(top_layout)
            main_layout.addLayout(bottom_layout)

            self.setLayout(main_layout)

            self.setWindowTitle("Reports Screen")
            self.setGeometry(100, 100, 1200, 900)
            self.setFixedSize(1200, 900)

            self.result1=''
            try:
                    cnx = mysql.connector.connect(user='bee', password='P@ssword', host='localhost',
                                                  auth_plugin='mysql_native_password', database='hmsdb')

                    cursor = cnx.cursor()

                    displayUsers_query = "SELECT nameofuser,surnameofuser,username,create_time, userroles FROM  users"
                    cursor.execute(displayUsers_query)
                    self.result1 = cursor.fetchall()
                    print(self.result1)

                    self.displayContent.setRowCount(5)
                    for row, item in enumerate(self.result1):
                            self.displayContent.insertRow(row)
                            for col, value in enumerate(item):
                                    table_item = QTableWidgetItem(str(value))

                                    self.displayContent.setItem(row, col, table_item)
                                    print(row, col, item)

                    finance_query = '''
                    SELECT customers.first_name,customers.last_name,customers.email,customers.phone,card_type,payments.card_no,payments.amount
                        FROM payments
                        JOIN customers on payments.customers_cust_id=customers.cust_id;
                    '''
                    cursor.execute(finance_query)
                    self.result1 = cursor.fetchall()
                    print(self.result1)

                    self.displayContentFinance.setRowCount(5)
                    for row, item in enumerate(self.result1):
                            self.displayContentFinance.insertRow(row)
                            for col, value in enumerate(item):
                                    table_item = QTableWidgetItem(str(value))

                                    self.displayContentFinance.setItem(row, col, table_item)
                                    print(row, col, item)
                    displayCustomers_query = "SELECT first_name,last_name, city,province,visite_type FROM customers"
                    cursor.execute(displayCustomers_query)
                    self.result1 = cursor.fetchall()
                    print(self.result1)

                    self.displayContentCustomer.setRowCount(5)
                    for row, item in enumerate(self.result1):
                            self.displayContentCustomer.insertRow(row)
                            for col, value in enumerate(item):
                                    table_item = QTableWidgetItem(str(value))

                                    self.displayContentCustomer.setItem(row, col, table_item)
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
                    cursor.close()
                    cnx.close()
                    print("Displayed Users")
    @pyqtSlot()
    def export_to_pdf(self, pdfkit=None):
            print("pdf button clicked!!!")
            pdf_file_path = r"C:\users\brendon\users.pdf"
            pdf = canvas.Canvas(pdf_file_path)
            pdf.drawString(100, 800, 'User Report')
            # Write data to PDF
            row_height = 20
            x = 30
            y = 780
            for row in self.result1:
                    for item in row:
                            pdf.drawString(x, y, str(item))
                            x += 120
                    y -= row_height
                    x = 30
            pdf.save()
            QMessageBox.information(self,"PDF saved ", pdf_file_path)

    def export_to_csv(self):

            print("csv button clicked!!!")
            csv_file_path = r"C:\users\brendon\users.csv"

            # Your data (replace this with your actual data)
            data = self.result1

            # Specify the CSV file path

            # Write data to CSV file
            with open(csv_file_path, 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerows(data)
                    QMessageBox.information(self, "CSV saved ", csv_file_path)

if __name__=='__main__':
    app= QApplication(sys.argv)
    window =reports()
    window.show()
    sys.exit(app.exec())