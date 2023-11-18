import os,sys

import mysql
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel,
                             QLineEdit, QPushButton, QGroupBox, QFormLayout,
                             QTableWidget, QVBoxLayout, QComboBox, QCalendarWidget, QMessageBox, QTableWidgetItem)
from pyqtgraph import PlotWidget, plot
from PyQt5.QtGui import QFont
import pyqtgraph as pg
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtGui import QFont
import mysql
import mysql.connector
from mysql.connector import connect, Error
from self import self

class analytics(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
            form = QFormLayout()

            # variables
            options_lbl = QLabel("Analysis")
            self.options_qcb = QComboBox()
            self.options_qcb.addItems(["","Customers"])
            self.options_qcb.setFixedWidth(300)
            math_lbl = QLabel("Operations")
            self.math_qcb = QComboBox()
            self.math_qcb.addItems(["","Average","Max","Min"])
            self.math_qcb.setFixedWidth(300)
            datesFrom_lbl = QLabel("Start Date")
            datesFrom_lbl.setFont(QFont('Arial',10))
            datesTo_lbl = QLabel("End Date")
            datesTo_lbl.setFont(QFont('Arial',10))
            dateFrom = QCalendarWidget()
            dateFrom.setFixedWidth(500)
            dateTo = QCalendarWidget()
            dateTo.setFixedWidth(500)
            datelineEditFrom = QLineEdit()
            datelineEditFrom.setPlaceholderText("start date")
            datelineEditFrom.setFixedWidth(300)
            datelineEditTo = QLineEdit()
            datelineEditTo.setPlaceholderText("end date")
            datelineEditTo.setFixedWidth(300)
            analytics_lne = QLineEdit()
            analytics_lne.setPlaceholderText("")
            analytics_lne.setFixedWidth(300)

            analytics_btn = QPushButton("Run")
            analytics_btn.setFixedWidth(300)
            self.displayStats=QLineEdit()
            self.displayStats.setFixedWidth(605)

            run_btn = QPushButton("Run")
            run_btn.setFixedWidth(300)
            run_btn.clicked.connect(self.statistics)

            qvb_layout = QVBoxLayout()

            form.addRow(options_lbl,self.options_qcb)
            form.addRow(math_lbl,self.math_qcb)
            form.addRow(datesFrom_lbl,datesTo_lbl)
            form.addRow(self.displayStats)
            form.addRow(run_btn)
            analytics_qgb = QGroupBox("Analytics")
            analytics_qgb.setLayout(form)
            qvb_layout.addWidget(analytics_qgb)
            self.setLayout(qvb_layout)

            self.setWindowTitle("Analytics screen")
            self.setGeometry(100, 100, 1200, 900)
            self.setFixedSize(1200, 900)


    # Stats method to get analysis
    @pyqtSlot()
    def statistics(self):
            print('Get Data Clicked!!!')
            print("getdata button clicked!!!")
            search_term = self.options_qcb.currentText()
            operation = self.math_qcb.currentText()
            print(operation)
            print(search_term)
            cnx = mysql.connector.connect(user='bee', password='P@ssword',
                                          host='localhost', auth_plugin='mysql_native_password',
                                          database='hmsdb')
            cursor = cnx.cursor()

            sql=("SELECT ROUND(AVG(cust_id)) FROM customers")
            max=("SELECT MAX(cust_id) FROM customers")
            min=("SELECT MIN(cust_id) FROM customers")

            if operation == "Average" and search_term == "Customers":
                #Calculate the average

                cursor.execute(sql)
                result = cursor.fetchone()
                self.displayStats.setText(f"{search_term}: {result[0]}")
                answer = self.displayStats.setText(f"{search_term}: {result[0]}")
                print(answer)
            elif operation == "Max" and search_term == "Customers":
                # Calculate the maximum
                cursor.execute(max)
                result = cursor.fetchone()
                self.displayStats.setText(f"{search_term}: {result[0]}")
                answer = self.displayStats.setText(f"{search_term}: {result[0]}")
                print(answer)
                #cursor.execute("SELECT MAX(cust_id) FROM customer")
            elif operation == "Min" and search_term == "Customers":
                # Calculate the maximum
                cursor.execute(min)
                result = cursor.fetchone()
                self.displayStats.setText(f"{search_term}: {result[0]}")
                answer = self.displayStats.setText(f"{search_term}: {result[0]}")
                print(answer)
            else:
                print("Not executed")

if __name__=='__main__':
    app= QApplication(sys.argv)
    window =analytics()
    window.show()
    sys.exit(app.exec())