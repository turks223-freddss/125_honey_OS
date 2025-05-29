from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
import sys
from collections import deque


class SchedulerSim(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PCB Scheduler Simulation")
        self.setGeometry(100, 100, 1000, 700)
        self.setup_ui()

        self.sim_timer = QtCore.QTimer()
        self.sim_timer.timeout.connect(self.simulate_step)
        self.sim_time = 0
        self.sim_processes = []
        self.sim_done = []
        self.sim_queue = deque()
        self.current_process = None
        self.quantum = 2
        self.quantum_counter = 0
        self.algorithm = ""

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.table = QtWidgets.QTableWidget(5, 3)
        self.table.setHorizontalHeaderLabels(["PID", "Arrival Time", "Burst Time"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(QtWidgets.QLabel("Enter Process Data:"))
        layout.addWidget(self.table)

        self.algorithm_box = QtWidgets.QComboBox()
        self.algorithm_box.addItems(["First Come First Serve", "Shortest Job First", "Round Robin", "SRPT"])
        layout.addWidget(QtWidgets.QLabel("Select Scheduling Algorithm:"))
        layout.addWidget(self.algorithm_box)

        self.quantum_input = QtWidgets.QLineEdit("2")
        layout.addWidget(QtWidgets.QLabel("Time Quantum (Only for RR):"))
        layout.addWidget(self.quantum_input)

        self.start_button = QtWidgets.QPushButton("Simulate")
        self.start_button.clicked.connect(self.simulate)
        layout.addWidget(self.start_button)

        self.result_table = QtWidgets.QTableWidget()
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels(["PID", "AT", "BT", "CT", "TAT", "WT"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(QtWidgets.QLabel("Result:"))
        layout.addWidget(self.result_table)

        # Visual timeline
        layout.addWidget(QtWidgets.QLabel("Simulation Timeline:"))
        self.timeline_container = QtWidgets.QScrollArea()
        self.timeline_widget = QtWidgets.QWidget()
        self.timeline_layout = QtWidgets.QHBoxLayout(self.timeline_widget)
        self.timeline_container.setWidgetResizable(True)
        self.timeline_container.setWidget(self.timeline_widget)
        layout.addWidget(self.timeline_container)

    def simulate(self):
        self.sim_processes = []
        for row in range(self.table.rowCount()):
            try:
                pid = str(self.table.item(row, 0).text())
                at = int(self.table.item(row, 1).text())
                bt = int(self.table.item(row, 2).text())
                self.sim_processes.append({"pid": pid, "at": at, "bt": bt, "remaining": bt})
            except:
                continue

        self.table.setRowCount(0)
        self.sim_time = 0
        self.sim_done = []
        self.sim_queue = deque()
        self.current_process = None
        self.quantum_counter = 0
        self.algorithm = self.algorithm_box.currentText()
        self.quantum = int(self.quantum_input.text()) if self.algorithm == "Round Robin" else None

        self.result_table.setRowCount(0)
        # Clear previous timeline
        for i in reversed(range(self.timeline_layout.count())):
            widget = self.timeline_layout.takeAt(i).widget()
            if widget:
                widget.setParent(None)
        # self.table.setVisible(False)  # 🔸 Hide input table during simulation
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.sim_timer.start(1000)

    def simulate_step(self):
        self.sim_time += 1
        # Add newly arriving processes
        arrivals = [p for p in self.sim_processes if p["at"] == self.sim_time - 1]
        for p in arrivals:
            self.sim_queue.append(p)
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(p["pid"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(p["at"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(p["bt"])))

        if self.algorithm == "First Come First Serve":
            self.run_fcfs()
        elif self.algorithm == "Shortest Job First":
            self.run_sjf()
        elif self.algorithm == "Round Robin":
            self.run_rr()
        elif self.algorithm == "SRPT":
            self.run_srpt()

        self.update_gui_table()
        self.setWindowTitle(f"Time: {self.sim_time} | Running: {self.current_process['pid'] if self.current_process else 'Idle'}")
        self.add_timeline_block(self.current_process["pid"] if self.current_process else "Idle")

        if len(self.sim_done) == len(self.sim_processes):
            self.sim_timer.stop()
            self.display_result()
    
    def update_gui_table(self):
        for row in range(self.table.rowCount()):
            pid_item = self.table.item(row, 0)
            if pid_item is None:
                continue
            pid = pid_item.text()
            for p in self.sim_queue:
                if p["pid"] == pid:
                    self.table.setItem(row, 2, QTableWidgetItem(str(p["remaining"])))
            if self.current_process and pid == self.current_process["pid"]:
                self.table.setItem(row, 2, QTableWidgetItem(str(self.current_process["remaining"])))

    def run_fcfs(self):
        if not self.current_process and self.sim_queue:
            self.current_process = self.sim_queue.popleft()

        if self.current_process:
            self.current_process["remaining"] -= 1
            if self.current_process["remaining"] == 0:
                self.finish_process()

    def run_sjf(self):
        if not self.current_process:
            if self.sim_queue:
                self.current_process = min(self.sim_queue, key=lambda x: x["bt"])
                self.sim_queue.remove(self.current_process)

        if self.current_process:
            self.current_process["remaining"] -= 1
            if self.current_process["remaining"] == 0:
                self.finish_process()

    def run_rr(self):
        if not self.current_process and self.sim_queue:
            self.current_process = self.sim_queue.popleft()
            self.quantum_counter = 0

        if self.current_process:
            self.current_process["remaining"] -= 1
            self.quantum_counter += 1

            if self.current_process["remaining"] == 0:
                self.finish_process()
            elif self.quantum_counter == self.quantum:
                self.sim_queue.append(self.current_process)
                self.current_process = None

    def run_srpt(self):
        all_ready = list(self.sim_queue)
        if self.current_process:
            all_ready.append(self.current_process)

        if all_ready:
            self.current_process = min(all_ready, key=lambda x: x["remaining"])
            all_ready.remove(self.current_process)
            self.sim_queue = deque(all_ready)

        if self.current_process:
            self.current_process["remaining"] -= 1
            if self.current_process["remaining"] == 0:
                self.finish_process()

    def finish_process(self):
        self.current_process["ct"] = self.sim_time
        self.current_process["tat"] = self.current_process["ct"] - self.current_process["at"]
        self.current_process["wt"] = self.current_process["tat"] - self.current_process["bt"]
        self.sim_done.append(self.current_process)

        # Remove from table
        for row in range(self.table.rowCount()):
            pid_item = self.table.item(row, 0)
            if pid_item and pid_item.text() == self.current_process["pid"]:
                self.table.removeRow(row)
                break

        self.current_process = None

    def display_result(self):
        self.result_table.setRowCount(len(self.sim_done))
        for i, p in enumerate(self.sim_done):
            for j, key in enumerate(["pid", "at", "bt", "ct", "tat", "wt"]):
                self.result_table.setItem(i, j, QTableWidgetItem(str(p[key])))
        self.setWindowTitle("Simulation Complete")
        self.table.setVisible(True)  # 🔸 Show input table when simulation ends
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)

    def add_timeline_block(self, pid):
        label = QtWidgets.QLabel(pid)
        label.setFixedSize(40, 30)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet(f"background-color: {self.get_color(pid)}; border: 1px solid black;")
        self.timeline_layout.addWidget(label)

    def get_color(self, pid):
        # Assign consistent color for each PID
        colors = {
            'A': '#FFA07A', 'B': '#20B2AA', 'C': '#87CEFA',
            'D': '#DDA0DD', 'E': '#98FB98', 'F': '#F4A460',
            'G': '#FFB6C1', 'H': '#B0C4DE', 'I': '#90EE90',
            'J': '#FFD700', 'Idle': '#D3D3D3'
        }
        return colors.get(pid.upper(), '#D3D3D3')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = SchedulerSim()
    win.show()
    sys.exit(app.exec_())
