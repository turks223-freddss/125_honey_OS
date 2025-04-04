import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread, Qt
import time
import random
import os
import numpy as np
from randomizer import table_randomizer
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget, QPushButton, QTabWidget, QLabel,  QDialog

from shortest_job_first import sjf
from collections import deque
from first_come_first_serve import fcfs
from priority import priority
# from round_robin import rr

# PCB class definition
class PCB:
    def __init__(self, pid, process_name, burst_time, memory_size, arrival_time, priority, status):
        self.pid = pid
        self.process_name = process_name
        self.burst_time = burst_time
        self.memory_size = memory_size
        self.arrival_time = arrival_time
        self.priority = priority
        self.status = status

    def change_status(self, new_status):
        self.status = new_status

    def get_name(self):
        return self.process_name

    def get_status(self):
        return self.status

    def get_burst(self):
        return self.burst_time
    
    def get_memory(self):
        return self.memory_size
    
    def get_pid(self):
        return self.pid
    
    def get_priority(self):
        return self.priority
    
    def get_arrival(self):
        return self.arrival_time
    
    def burst_decrement(self):
        if self.burst_time > 0:
            self.burst_time -= 1

        if self.burst_time == 0:
            self.change_status("Terminate")

def display_pcb_table(main_window, pcb_array, scheduling_type):
    # Filter out terminated processes
    active_processes = [pcb for pcb in pcb_array if pcb.get_status() != "Terminate"]
    
    main_window.table_widget.setRowCount(len(active_processes))
    for row_idx, pcb in enumerate(active_processes):
        row_data = [
            pcb.pid, pcb.process_name, pcb.burst_time, pcb.memory_size,
            pcb.arrival_time, pcb.priority, pcb.status
        ]
        # Hide the priority column for scheduling types other than 'ps'
        if scheduling_type != 'ps' and scheduling_type != 'sjfp' :
            row_data.pop(5)  # Remove priority from the row data
        for col_idx, item in enumerate(row_data):
            main_window.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))
    # Hide priority column if scheduling type is not 'ps'
    if scheduling_type != 'ps' and scheduling_type != 'sjfp' :
        main_window.table_widget.hideColumn(5)  # Hide the priority column
    else:
        main_window.table_widget.showColumn(5)  # Show the priority column if scheduling type is 'ps'

def generate_random_pcb(pid, unique_priorities, scheduling_type):
    randomizer = table_randomizer()
    process_name = randomizer.pick_process
    burst_time = randomizer.burst_time
    memory_size = randomizer.memory_size
    
    if scheduling_type == 'ps':
        priority = unique_priorities.pop()
    else:
        priority = unique_priorities.pop(0)  # Ensure non-zero priority for other scheduling types

    # Status set to "New"
    status = "New"
    return PCB(pid, process_name, burst_time, memory_size, pid - 1, priority, status)

def update_arrival_times(pcb_array):
    for pcb in pcb_array:
        if pcb.arrival_time > 0:
            pcb.arrival_time -= 1

# Worker class to handle the processing in a separate thread
class Worker(QThread):
    update_table_signal = pyqtSignal(object)  # Signal to update the table in the GUI

    def __init__(self, main_window, num_processes, scheduling_type):
        super().__init__()
        self.main_window = main_window
        self.num_processes = num_processes
        self.scheduling_type = scheduling_type

    def run(self):
        unique_priorities = list(range(1, self.num_processes + 1))
        unique_priorities = [value for value in unique_priorities for _ in range(2)]
        unique_priorities = unique_priorities[:self.num_processes]
        random.shuffle(unique_priorities)

        pcb_array = np.empty(self.num_processes, dtype=object)

        if self.scheduling_type == 'fcfs':
            unique_priorities = [0] * self.num_processes
            for pid in range(1, self.num_processes + 1):
                if pid > 1:
                    pcb_array[pid - 2].status = "Waiting"

                # pcb = generate_random_pcb(pid, unique_priorities)
                pcb = generate_random_pcb(pid, unique_priorities, self.scheduling_type)
                pcb_array[pid - 1] = pcb

                os.system('cls' if os.name == 'nt' else 'clear')

                fcfs(pcb_array[:pid], pid - 1, self.num_processes, self.update_table_signal)

                self.update_table_signal.emit(pcb_array[:pid])
                display_pcb_table(self.main_window, pcb_array[:pid], self.scheduling_type)

                time.sleep(1)

            display_pcb_table(self.main_window, pcb_array, self.scheduling_type)
            self.update_table_signal.emit(pcb_array)

        elif self.scheduling_type == 'sjf':
            unique_priorities = [0] * self.num_processes
            for pid in range(1, self.num_processes + 1):
                if pid > 1:
                    pcb_array[pid - 2].status = "Waiting"

                # pcb = generate_random_pcb(pid, unique_priorities)
                pcb = generate_random_pcb(pid, unique_priorities, self.scheduling_type)
                pcb_array[pid - 1] = pcb

                os.system('cls' if os.name == 'nt' else 'clear')

                sjf(pcb_array[:pid], pid - 1, self.num_processes, self.update_table_signal)

                self.update_table_signal.emit(pcb_array[:pid])
                display_pcb_table(self.main_window, pcb_array[:pid], self.scheduling_type)

                time.sleep(1)

            display_pcb_table(self.main_window, pcb_array, self.scheduling_type)
            self.update_table_signal.emit(pcb_array)

        elif self.scheduling_type == 'rr':
            unique_priorities = [0] * self.num_processes
            queue = deque()

            for pid in range(1, self.num_processes + 1):
                if pid > 1:
                    pcb_array[pid - 2].status = "Waiting"

                # pcb = generate_random_pcb(pid, unique_priorities)
                pcb = generate_random_pcb(pid, unique_priorities, self.scheduling_type)
                pcb_array[pid - 1] = pcb

                queue.append(pcb)

            os.system('cls' if os.name == 'nt' else 'clear')

            quantum = 2  # You've set the quantum time to 2 seconds

            total_burst_time = sum(pcb.burst_time for pcb in pcb_array)

            while total_burst_time > 0:
                current_process = queue.popleft()

                # Set the status of the current process to "Running"
                current_process.change_status("Running")

                for _ in range(min(quantum, current_process.burst_time)):
                    time.sleep(1)
                    current_process.burst_decrement()
                    total_burst_time -= 1

                    self.update_table_signal.emit(pcb_array)

                    if current_process.burst_time == 0:
                        current_process.change_status("Terminate")
                        break
                else:
                    # Put the current process back to the end of the queue
                    queue.append(current_process)

                # Set the status of other processes in the queue to "Ready"
                for process in queue:
                    process.change_status("Ready")

            self.update_table_signal.emit(pcb_array)


        elif self.scheduling_type == 'ps':
            for pid in range(1, self.num_processes + 1):
                if pid > 1:
                    pcb_array[pid - 2].status = "Waiting"

                # pcb = generate_random_pcb(pid, unique_priorities)
                pcb = generate_random_pcb(pid, unique_priorities, self.scheduling_type)
                pcb_array[pid - 1] = pcb

                os.system('cls' if os.name == 'nt' else 'clear')

                priority(pcb_array[:pid], pid - 1, self.num_processes, self.update_table_signal)

                self.update_table_signal.emit(pcb_array[:pid])
                display_pcb_table(self.main_window, pcb_array[:pid], self.scheduling_type)

                time.sleep(1)

            display_pcb_table(self.main_window, pcb_array, self.scheduling_type)
            self.update_table_signal.emit(pcb_array)
        
        elif self.scheduling_type == 'sjfp':
            for pid in range(1, self.num_processes + 1):
                if pid > 1:
                    pcb_array[pid - 2].status = "Waiting"

                # pcb = generate_random_pcb(pid, unique_priorities)
                pcb = generate_random_pcb(pid, unique_priorities, self.scheduling_type)
                pcb_array[pid - 1] = pcb

                os.system('cls' if os.name == 'nt' else 'clear')

                sjf(pcb_array[:pid], pid - 1, self.num_processes, self.update_table_signal)

                self.update_table_signal.emit(pcb_array[:pid])
                display_pcb_table(self.main_window, pcb_array[:pid], self.scheduling_type)

                time.sleep(1)

            display_pcb_table(self.main_window, pcb_array, self.scheduling_type)
            self.update_table_signal.emit(pcb_array)

# GUI WINDOW
class MainWindow(QMainWindow):
    def __init__(self, headers):
        super().__init__()
        loadUi("SCHEDULEGUI/scheduler.ui", self)

        self.headers = headers

        # Get reference to the QTabWidget and QLabel
        self.tabWidget = self.findChild(QTabWidget, "tabWidget_2")
        print("tabWidget:", self.tabWidget)  # Debugging print statement

        if self.tabWidget is None:
            print("Error: 'tabWidget' not found")
        else:
            self.label = self.findChild(QLabel, "label_2")
            print("label:", self.label)  # Debugging print statement

            if self.label is None:
                print("Error: 'label_2' not found")
            else:
                # Connect the currentChanged signal to the updateLabel method
                self.tabWidget.currentChanged.connect(self.updateLabel)
                # Update the label initially
                self.updateLabel()

        self.initUI()
    
    def initUI(self):
        self.tab_widget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_2')
        self.tab_widget.currentChanged.connect(self.onTabChanged)
        self.setupTab(self.tab_widget.currentIndex())
        self.setWindowTitle("PrettyTable to QTableWidget")
        self.show()

    def onTabChanged(self, index):
        self.setupTab(index)

    def setupTab(self, index):
        current_tab = self.tab_widget.widget(index)
        print(f"User switched to tab index {index}, object name: {current_tab.objectName()}")

        if current_tab.objectName() == 'tab_5':
            self.table_widget = current_tab.findChild(QTableWidget, "tableWidget")
            self.start_button = current_tab.findChild(QtWidgets.QPushButton, 'pushButton_9')
            self.scheduling_type = 'fcfs'
            print("This is tab_5")
        elif current_tab.objectName() == 'tab_6':
            self.table_widget = current_tab.findChild(QTableWidget, "tableWidget_3")
            self.start_button = current_tab.findChild(QtWidgets.QPushButton, 'pushButton_11')
            self.scheduling_type = 'sjf'
            print("This is tab_6")
        elif current_tab.objectName() == 'tab_7':
            self.table_widget = current_tab.findChild(QTableWidget, "tableWidget_5")
            self.start_button = current_tab.findChild(QtWidgets.QPushButton, 'pushButton_12')
            self.scheduling_type = 'ps'
            print("This is tab_7")
        elif current_tab.objectName() == 'tab_8':
            self.table_widget = current_tab.findChild(QTableWidget, "tableWidget_7")
            self.start_button = current_tab.findChild(QtWidgets.QPushButton, 'pushButton_13')
            self.scheduling_type = 'rr'
            print("This is tab_8")
        elif current_tab.objectName() == 'tab':
            self.table_widget = current_tab.findChild(QTableWidget, "tableWidget_9")
            self.start_button = current_tab.findChild(QtWidgets.QPushButton, 'pushButton_14')
            self.scheduling_type = 'sjfp'
            print("This is tab")
        else:
            self.table_widget = None
            self.start_button = None
            print("No specific tab found.")

        if self.table_widget:
            self.table_widget.setColumnCount(len(self.headers))
            self.table_widget.setHorizontalHeaderLabels(self.headers)

        if self.start_button:
            self.start_button.clicked.connect(self.start_process_generation)
        else:
            print("No start button found in the current tab.")

    def start_process_generation(self):
        num_processes = random.randint(4, 6)
        self.worker = Worker(self, num_processes, self.scheduling_type)
        self.worker.update_table_signal.connect(self.update_table)
        self.worker.start()

    def update_table(self, pcb_array):
        active_processes = [pcb for pcb in pcb_array if pcb.get_status() != "Terminate"]
        self.table_widget.setRowCount(len(active_processes))
        for row_idx, pcb in enumerate(active_processes):
            row_data = [
                pcb.pid, pcb.process_name, pcb.burst_time, pcb.memory_size,
                pcb.arrival_time, pcb.priority, pcb.status
            ]
            for col_idx, item in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

    def updateLabel(self):
        # Get the current tab text and set it as the label text
        current_tab = self.tabWidget.currentWidget()
        current_tab_title = self.tabWidget.tabText(self.tabWidget.indexOf(current_tab))
        self.label.setText(current_tab_title)

    # Connect buttons to slots
        self.exitBtn.clicked.connect(self.exit_app)
        self.minimizeBtn.clicked.connect(self.minimize_app)

        # Hide the toolbar (title bar)
        self.setWindowFlag(Qt.FramelessWindowHint)

    def exit_app(self):
        # Function to exit the application
        app.quit()

    def minimize_app(self):
        # Function to minimize the main window
        self.showMinimized()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    headers = ["PID", "Process Name", "Burst Time", "Memory Size", "Arrival Time", "Priority", "Status"]
    mainWindow = MainWindow(headers)
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainWindow)
    widget.setFixedHeight(858)
    widget.setFixedWidth(1310)
    widget.show()

    try:
        print("Opening App")
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Exiting due to error: {e}")