from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
import sys
from collections import deque
import random


class SchedulerSim(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PCB Scheduler Simulation")
        self.setGeometry(100, 100, 1000, 700)
        
        self.total_memory_mb = 500
        self.block_size_mb = 20
        self.total_blocks = self.total_memory_mb // self.block_size_mb
        self.memory_blocks = [None] * self.total_blocks  # None means free block, else stores pid
        
        self.setup_ui()

        self.sim_timer = QtCore.QTimer()
        self.sim_timer.timeout.connect(self.simulate_step)
        self.sim_time = 0
        self.sim_processes = []
        self.sim_done = []
        self.sim_queue = deque()
        self.running_processes = []  # instead of self.current_process
        self.quantum = 2
        self.quantum_counter = 0
        self.algorithm = ""
        
        
    def setup_ui(self):
        main_layout = QtWidgets.QHBoxLayout(self)  # Horizontal main layout

        left_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(left_layout, stretch=3)  # left side bigger

        # Move all your current widgets except memory_table into left_layout:
        self.table = QtWidgets.QTableWidget(10, 4)
        self.table.setHorizontalHeaderLabels(["PID", "Arrival Time", "Burst Time", "Memory"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        left_layout.addWidget(QtWidgets.QLabel("Enter Process Data:"))
        left_layout.addWidget(self.table)

        self.algorithm_box = QtWidgets.QComboBox()
        self.algorithm_box.addItems(["First Come First Serve", "Shortest Job First", "Round Robin", "SRPT"])
        left_layout.addWidget(QtWidgets.QLabel("Select Scheduling Algorithm:"))
        left_layout.addWidget(self.algorithm_box)

        self.quantum_input = QtWidgets.QLineEdit("2")
        left_layout.addWidget(QtWidgets.QLabel("Time Quantum (Only for RR):"))
        left_layout.addWidget(self.quantum_input)

        self.start_button = QtWidgets.QPushButton("Simulate")
        self.start_button.clicked.connect(self.simulate)
        left_layout.addWidget(self.start_button)

        self.result_table = QtWidgets.QTableWidget()
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels(["PID", "AT", "BT", "CT", "TAT", "WT"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        left_layout.addWidget(QtWidgets.QLabel("Result:"))
        left_layout.addWidget(self.result_table)

        # left_layout.addWidget(QtWidgets.QLabel("Simulation Timeline:"))
        # self.timeline_container = QtWidgets.QScrollArea()
        # self.timeline_widget = QtWidgets.QWidget()
        # self.timeline_layout = QtWidgets.QHBoxLayout(self.timeline_widget)
        # self.timeline_container.setWidgetResizable(True)
        # self.timeline_container.setWidget(self.timeline_widget)
        # left_layout.addWidget(self.timeline_container)

        # Now the memory table on the right, vertically:
        self.memory_table = QtWidgets.QTableWidget(self.total_blocks, 1)  # rows = blocks, cols = 1
        self.memory_table.setFixedWidth(200)
        self.memory_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.memory_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.memory_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.memory_table.setHorizontalHeaderLabels(["Mem Blocks"])
        self.memory_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.memory_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.memory_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        main_layout.addWidget(self.memory_table, stretch=1)

    def simulate(self):
        self.sim_processes = []
        list_of_processes = [
            "Spotify", "Calculator", "Google Chrome", "Camera", "Bumble", "Microsoft Excel", 
            "Microsoft Edge", "Discord", "Facebook", "Messenger", "Skype", "Steam", "FireFox", 
            "Task Manager", "VLC Media Player", "Microsoft Word", "Microsoft Powerpoint", "Microsoft Office", 
            "Microsoft Outlook", "Microsoft Teams", "Bookworm Adventures", "Adobe Photoshop", 
            "Adobe Premiere Pro", "Adobe Edition", "Adobe Illustrator", "Zoom", "Google Meet", 
            "WPS", "Microsoft OneDrive", "Adobe Reader and Acrobat Manager", "Adobe After Effects", 
            "CheatEngine", "Ibis Paint", "Visual Studio Code", "GitHub Desktop", "CLion", "Sublime Text", 
            "Notepad++", "Notepad", "System Settings", "Command Prompt", "Powershell", "Opera GX", "File Explorer", 
            "PuTTy", "WinRar", "Oracle VM Box", "Team Viewer", "Tindr", "Blender", "SketchUp", "Unity", "PyCharm", 
            "Eclipse", "NetBeans", "MySQL Server", "MySQL Workbench", "XAMPP Control Panel", "PowerPlanner", 
            "Solitaire", "Calendar", "Clock", "Git", "OBS Studio", "Sticky Notes", "Tekken", "Skull Girls", 
            "Stardew Valley", "Sound Recorder", "Snipping Tool", "Terminal", "Zotero", "MechaVibes", 
            "Youtube", "Instagram", "Tiktok", "X", "Linkedin", "Capcut", "Netflix", "Honkai Star Rail", 
            "Genshin Impact", "League of Legends", "Dota 2", "Crossfire", "Counter Strike", "Call of Duty", 
            "Last of Us", "The Sims 4", "Grammarly", "Notion", "Trello"
        ]
        # Auto-fill table with random processes if it's empty
        if all(self.table.item(row, 0) is None for row in range(self.table.rowCount())):
            self.table.setRowCount(10)
            used_process_names = set()
            random.shuffle(list_of_processes)
            for row in range(10):
                # Ensure unique PID (like A, B, C...)
                process_name = list_of_processes.pop()  # Unique name
                used_process_names.add(process_name)
                at = random.randint(0, 10)
                bt = random.randint(1, 10)
                mem = random.choice([20, 40, 60, 80, 100, 120])
                self.table.setItem(row, 0, QTableWidgetItem(process_name))
                self.table.setItem(row, 1, QTableWidgetItem(str(at)))
                self.table.setItem(row, 2, QTableWidgetItem(str(bt)))
                self.table.setItem(row, 3, QTableWidgetItem(str(mem)))
                
        for row in range(self.table.rowCount()):
            try:
                pid = str(self.table.item(row, 0).text())
                at = int(self.table.item(row, 1).text())
                bt = int(self.table.item(row, 2).text())
                mem = int(self.table.item(row, 3).text())
                self.sim_processes.append({"pid": pid, "at": at, "bt": bt, "remaining": bt, "mem":mem})
            except:
                continue

        
        self.sim_time = 0
        self.sim_done = []
        self.sim_queue = deque()
        self.running_processes = []
        self.quantum_counter = 0
        self.algorithm = self.algorithm_box.currentText()
        self.quantum = int(self.quantum_input.text()) if self.algorithm == "Round Robin" else None

        self.result_table.setRowCount(0)
        # Clear previous timeline
        # for i in reversed(range(self.timeline_layout.count())):
        #     widget = self.timeline_layout.takeAt(i).widget()
        #     if widget:
        #         widget.setParent(None)
        # self.table.setVisible(False)  # 🔸 Hide input table during simulation
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.sim_timer.start(1000)
        
        self.memory_blocks = [None] * self.total_blocks
        self.update_memory_table()

    def simulate_step(self):
        self.sim_time += 1

        # Add newly arriving processes to queue
        arrivals = [p for p in self.sim_processes if p["at"] == self.sim_time - 1]
        for p in arrivals:
            self.sim_queue.append(p)

        # Try to allocate memory and start processes from queue
        new_queue = deque()
        for p in self.sim_queue:
            mem_needed = p["mem"]
            blocks_needed = (mem_needed + self.block_size_mb - 1) // self.block_size_mb
            allocated = self.allocate_memory(p["pid"], blocks_needed)
            if allocated:
                p["mem_allocated"] = True
                self.running_processes.append(p)
            else:
                new_queue.append(p)  # Not enough memory, stay in queue
        self.sim_queue = new_queue

        # Run all running processes (simulate concurrency)
        finished = []
        for p in self.running_processes:
            # For RR and SRPT, implement logic here if needed (else assume all run)
            p["remaining"] -= 1
            if p["remaining"] <= 0:
                finished.append(p)

        # Finish processes and free memory
        for p in finished:
            self.finish_process(p)
            self.running_processes.remove(p)

        self.update_gui_table()

        running_pids = ', '.join(p['pid'] for p in self.running_processes) if self.running_processes else 'Idle'
        self.setWindowTitle(f"Time: {self.sim_time} | Running: {running_pids}")

        if len(self.sim_done) == len(self.sim_processes):
            self.sim_timer.stop()
            self.display_result()

        self.update_memory_table()
    
    def update_gui_table(self):
        for row in range(self.table.rowCount()):
            pid_item = self.table.item(row, 0)
            if pid_item is None:
                continue
            pid = pid_item.text()
            for p in self.sim_queue:
                if p["pid"] == pid:
                    self.table.setItem(row, 2, QTableWidgetItem(str(p["remaining"])))
            for p in self.running_processes:
                if pid == p["pid"]:
                    self.table.setItem(row, 2, QTableWidgetItem(str(p["remaining"])))

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
                
    def allocate_memory(self, pid, blocks_needed):
        # Find continuous free blocks? or just enough free blocks anywhere
        free_indices = [i for i, b in enumerate(self.memory_blocks) if b is None]
        if len(free_indices) < blocks_needed:
            return False  # Not enough memory

        # Allocate first 'blocks_needed' free blocks (simple First Fit)
        allocated_blocks = free_indices[:blocks_needed]
        for idx in allocated_blocks:
            self.memory_blocks[idx] = pid
        return True

    def free_memory(self, pid):
        for i in range(len(self.memory_blocks)):
            if self.memory_blocks[i] == pid:
                self.memory_blocks[i] = None

    def update_memory_table(self):
        for row in range(self.total_blocks):
            pid = self.memory_blocks[row]
            item = QTableWidgetItem(pid if pid else "")
            if pid:
                item.setBackground(QtGui.QColor(self.get_color(pid)))
            else:
                item.setBackground(QtGui.QColor("#FFFFFF"))
            self.memory_table.setItem(row, 0, item)

    def finish_process(self, process):
        process["ct"] = self.sim_time
        process["tat"] = process["ct"] - process["at"]
        process["wt"] = process["tat"] - process["bt"]
        self.sim_done.append(process)

        # Free memory blocks
        for i in range(len(self.memory_blocks)):
            if self.memory_blocks[i] == process["pid"]:
                self.memory_blocks[i] = None

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
