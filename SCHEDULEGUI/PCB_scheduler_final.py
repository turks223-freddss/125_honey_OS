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
        
        self.ready_queue = deque()
        self.current_process = None
        
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
        
    def apply_bee_theme(self):
        bee_style = """
            QWidget {
                background-color: #fff8dc;  /* light yellow */
                font-family: Arial;
                font-size: 14px;
            }

            QTableWidget {
                background-color: #ffffe0; /* lemon chiffon */
                gridline-color: #d4af37;  /* honey gold */
            }

            QTableWidget::item {
                selection-background-color: #ffd700;  /* gold */
            }

            QHeaderView::section {
                background-color: #ffcc00;
                color: black;
                padding: 4px;
                border: 1px solid #d4af37;
            }

            QPushButton {
                background-color: #ffcc00;
                color: black;
                border: 2px solid #d4af37;
                border-radius: 8px;
                padding: 5px 10px;
            }

            QPushButton:hover {
                background-color: #ffd700;
            }

            QComboBox {
                background-color: #fffacd;  /* light yellow */
                border: 1px solid #d4af37;
                padding: 4px;
            }

            QLineEdit {
                background-color: #fffacd;
                border: 1px solid #d4af37;
                padding: 4px;
            }

            QLabel {
                font-weight: bold;
                color: #222;
            }
        """
        self.setStyleSheet(bee_style)

    
    def setup_ui(self):
        main_layout = QtWidgets.QHBoxLayout(self)  # Horizontal main layout

        left_layout = QtWidgets.QVBoxLayout()
        right_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(left_layout, stretch=3)  # left side bigger
        main_layout.addLayout(right_layout, stretch=1)  # right side smaller

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
        
        self.reset_button = QtWidgets.QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_simulation)
        left_layout.addWidget(self.reset_button)

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
        self.memory_table.setHorizontalHeaderLabels(["Mem Blocks (500mb)"])
        self.memory_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.memory_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.memory_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        right_layout.addWidget(self.memory_table)

        right_layout.addWidget(QtWidgets.QLabel("Memory Allocation Strategy:"))

        self.allocation_strategy_box = QtWidgets.QComboBox()
        self.allocation_strategy_box.addItems(["First-Fit", "Best-Fit", "Worst-Fit"])
        right_layout.addWidget(self.allocation_strategy_box)
        
        self.apply_bee_theme()

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
                mem = random.choice([25, 45, 60, 80, 100, 120])
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

        # Add newly arriving processes to sim_queue
        arrivals = [p for p in self.sim_processes if p["at"] == self.sim_time - 1]
        for p in arrivals:
            self.sim_queue.append(p)

        # Try to allocate memory for processes in sim_queue
        new_sim_queue = deque()
        for p in self.sim_queue:
            mem_needed = p["mem"]
            blocks_needed = (mem_needed + self.block_size_mb - 1) // self.block_size_mb
            allocated = self.allocate_memory(p["pid"], blocks_needed)
            if allocated:
                p["mem_allocated"] = True
                self.ready_queue.append(p)  # loaded, ready for CPU
            else:
                new_sim_queue.append(p)
        self.sim_queue = new_sim_queue

        # Pick next process to run based on scheduling algo
        if not self.current_process or self.current_process["remaining"] <= 0 or (self.algorithm == "Round Robin" and self.quantum_counter == self.quantum):
            if self.current_process and self.current_process["remaining"] > 0:
                # for RR, put current back in ready queue if not done
                if self.algorithm == "Round Robin":
                    self.ready_queue.append(self.current_process)
            # Pick next process according to algorithm from ready_queue
            self.current_process = self.pick_next_process()

            # Reset RR quantum counter
            if self.algorithm == "Round Robin":
                self.quantum_counter = 0

        # Run current_process
        if self.current_process:
            self.current_process["remaining"] -= 1
            if self.algorithm == "Round Robin":
                self.quantum_counter += 1

            if self.current_process["remaining"] <= 0:
                self.finish_process(self.current_process)
                self.current_process = None

        # Update GUI and memory visualization
        self.update_gui_table()
        self.update_memory_table()

        # Update window title
        running_pid = self.current_process["pid"] if self.current_process else "Idle"
        self.setWindowTitle(f"Time: {self.sim_time} | Running: {running_pid}")

        # End simulation check
        if len(self.sim_done) == len(self.sim_processes):
            self.sim_timer.stop()
            self.display_result()
    
    def update_gui_table(self):
        for row in range(self.table.rowCount()):
            pid_item = self.table.item(row, 0)
            if pid_item is None:
                continue
            pid = pid_item.text()

            # Check current_process first
            if self.current_process and self.current_process["pid"] == pid:
                self.table.setItem(row, 2, QTableWidgetItem(str(self.current_process["remaining"])))
                continue
            
            # Check ready_queue for process with this pid
            for p in self.ready_queue:
                if p["pid"] == pid:
                    self.table.setItem(row, 2, QTableWidgetItem(str(p["remaining"])))
                    break
            else:
                # If process is finished or not found, optionally reset to 0 or original burst time
                pass
    
    def pick_next_process(self):
        if not self.ready_queue:
            return None

        if self.algorithm == "First Come First Serve":
            return self.ready_queue.popleft()
        elif self.algorithm == "Shortest Job First":
            # Pick shortest burst time
            shortest = min(self.ready_queue, key=lambda p: p["bt"])
            self.ready_queue.remove(shortest)
            return shortest
        elif self.algorithm == "Round Robin":
            return self.ready_queue.popleft()
        elif self.algorithm == "SRPT":
            # Preemptive shortest remaining time
            if self.current_process:
                all_ready = list(self.ready_queue) + [self.current_process]
            else:
                all_ready = list(self.ready_queue)
            shortest = min(all_ready, key=lambda p: p["remaining"])
            # Remove chosen from ready_queue if it's there
            if shortest in self.ready_queue:
                self.ready_queue.remove(shortest)
            # If chosen is not current_process, push current back to ready_queue
            if self.current_process and self.current_process != shortest:
                self.ready_queue.append(self.current_process)
            return shortest

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
        strategy = self.allocation_strategy_box.currentText()

        # Find free memory blocks based on strategy
        if strategy == "First-Fit":
            start_index = self.find_first_fit(blocks_needed)
        elif strategy == "Best-Fit":
            start_index = self.find_best_fit(blocks_needed)
        elif strategy == "Worst-Fit":
            start_index = self.find_worst_fit(blocks_needed)
        else:
            start_index = None

        if start_index is None:
            return False  # No sufficient free block found

        # Allocate blocks to process
        for i in range(start_index, start_index + blocks_needed):
            self.memory_blocks[i] = pid
        return True
    
    def find_first_fit(self, blocks_needed):
        free_count = 0
        start_index = 0
        for i, block in enumerate(self.memory_blocks):
            if block is None:
                if free_count == 0:
                    start_index = i
                free_count += 1
                if free_count >= blocks_needed:
                    return start_index
            else:
                free_count = 0
        return None

    def find_best_fit(self, blocks_needed):
        free_blocks = []
        free_count = 0
        start_index = 0

        # Collect all free blocks ranges
        for i, block in enumerate(self.memory_blocks + [1]):  # Add sentinel to flush last run
            if block is None:
                if free_count == 0:
                    start_index = i
                free_count += 1
            else:
                if free_count >= blocks_needed:
                    free_blocks.append((free_count, start_index))
                free_count = 0

        if not free_blocks:
            return None

        # Pick the smallest free block range that fits the request
        free_blocks.sort(key=lambda x: x[0])
        return free_blocks[0][1]

    def find_worst_fit(self, blocks_needed):
        free_blocks = []
        free_count = 0
        start_index = 0

        # Collect all free blocks ranges
        for i, block in enumerate(self.memory_blocks + [1]):  # Add sentinel to flush last run
            if block is None:
                if free_count == 0:
                    start_index = i
                free_count += 1
            else:
                if free_count >= blocks_needed:
                    free_blocks.append((free_count, start_index))
                free_count = 0

        if not free_blocks:
            return None

        # Pick the largest free block range that fits the request
        free_blocks.sort(key=lambda x: x[0], reverse=True)
        return free_blocks[0][1]

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

    def reset_simulation(self):
        # Stop simulation timer
        self.sim_timer.stop()

        # Clear input process table
        self.table.clearContents()
        self.table.setRowCount(10)  # reset rows if you want
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)

        # Clear result table
        self.result_table.clearContents()
        self.result_table.setRowCount(0)

        # Clear memory blocks & update memory table
        self.memory_blocks = [None] * self.total_blocks
        self.update_memory_table()

        # Reset internal states
        self.sim_processes = []
        self.ready_queue.clear()
        self.sim_queue.clear()
        self.running_processes = []
        self.current_process = None
        self.sim_time = 0
        self.quantum_counter = 0

        # Reset window title
        self.setWindowTitle("PCB Scheduler Simulation")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = SchedulerSim()
    win.show()
    sys.exit(app.exec_())
