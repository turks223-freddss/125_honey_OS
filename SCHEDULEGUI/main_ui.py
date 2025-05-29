# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from main import main
from worker import WorkerThread
from PyQt5.QtWidgets import QTableWidgetItem


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Table setup
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 60, 1100, 321))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(8)

        # Create vertical header items
        for i in range(8):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i, item)

        # Create horizontal header items
        for i in range(7):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)

        # Buttons for scheduling algorithms
        self.sjfButton = QtWidgets.QPushButton(self.centralwidget)
        self.sjfButton.setGeometry(QtCore.QRect(20, 10, 150, 30))
        self.sjfButton.setObjectName("sjfButton")

        self.fcfsButton = QtWidgets.QPushButton(self.centralwidget)
        self.fcfsButton.setGeometry(QtCore.QRect(180, 10, 150, 30))
        self.fcfsButton.setObjectName("fcfsButton")

        self.rrButton = QtWidgets.QPushButton(self.centralwidget)
        self.rrButton.setGeometry(QtCore.QRect(340, 10, 150, 30))
        self.rrButton.setObjectName("rrButton")

        self.anotherButton = QtWidgets.QPushButton(self.centralwidget)
        self.anotherButton.setGeometry(QtCore.QRect(500, 10, 150, 30))
        self.anotherButton.setObjectName("anotherButton")

        # Example label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 400, 47, 14))
        self.label.setObjectName("label")

        # Menu bar and status bar
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 837, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        # Connect buttons
        self.sjfButton.clicked.connect(self.run_sjf)
        self.fcfsButton.clicked.connect(self.run_fcfs)
        self.rrButton.clicked.connect(lambda: print("Round Robin clicked"))
        self.anotherButton.clicked.connect(lambda: print("Another clicked"))

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def run_sjf(self):
        self.worker = WorkerThread(5, mode="fcfs")  # or get dynamic input
        self.worker.update_gui_signal.connect(self.update_table)
        self.worker.start()
        
    
    def run_fcfs(self):
        self.worker = WorkerThread(5, mode="fcfs")  # or get dynamic input
        self.worker.update_gui_signal.connect(self.update_table)
        self.worker.start()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Process Scheduler"))

        for i in range(8):
            item = self.tableWidget.verticalHeaderItem(i)
            item.setText(_translate("MainWindow", f"{i+1}"))

        headers = ["PID", "Burst Time", "Process Name", "Memory Size", "Arrival Time", "Priority", "Status"]
        for i, header in enumerate(headers):
            item = self.tableWidget.horizontalHeaderItem(i)
            item.setText(_translate("MainWindow", header))

        self.sjfButton.setText(_translate("MainWindow", "Short Job First"))
        self.fcfsButton.setText(_translate("MainWindow", "First Come First Serve"))
        self.rrButton.setText(_translate("MainWindow", "Round Robin"))
        self.anotherButton.setText(_translate("MainWindow", "Another"))
        self.label.setText(_translate("MainWindow", "Update"))

    def update_table(self, pcb_array):
        self.tableWidget.setRowCount(len(pcb_array))
        for row, pcb in enumerate(pcb_array):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(pcb.pid)))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(pcb.burst_time)))    # Burst Time
            self.tableWidget.setItem(row, 2, QTableWidgetItem(pcb.process_name))      # Process Name
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str(pcb.memory_size)))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(str(pcb.arrival_time)))
            self.tableWidget.setItem(row, 5, QTableWidgetItem(str(pcb.priority)))
            self.tableWidget.setItem(row, 6, QTableWidgetItem(pcb.status))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
