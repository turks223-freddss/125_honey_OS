import sys
import random
from PyQt5 import QtWidgets
from sampleui import Ui_MainWindow  # Import the UI class from sample.py

class PCB:
    def __init__(self, pid, burst_time, memory_size, arrival_time, priority, status):
        self.pid = pid
        self.burst_time = burst_time
        self.memory_size = memory_size
        self.arrival_time = arrival_time
        self.priority = priority
        self.status = status

def generate_random_pcb(pid):
    burst_time = random.randint(1, 20)
    memory_size = random.randint(1, 100)
    arrival_time = random.randint(0, 50)
    priority = random.randint(1, 10)
    status = "Ready"
    return PCB(pid, burst_time, memory_size, arrival_time, priority, status)

class MyMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.populate_table()

    def populate_table(self):
        pcb_list = [generate_random_pcb(pid) for pid in range(1, 8)]
        self.tableWidget.setRowCount(len(pcb_list))
        for row, pcb in enumerate(pcb_list):
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(pcb.pid)))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(pcb.burst_time)))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(pcb.memory_size)))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(pcb.arrival_time)))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(pcb.priority)))
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(pcb.status))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
