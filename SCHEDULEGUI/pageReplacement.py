from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLineEdit, QPushButton, QMessageBox, QLabel, QVBoxLayout, QHBoxLayout, QComboBox
import sys
from collections import deque

class MemoryCanvas(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.memory = []
        self.slot_size_mb = 20
        self.total_slots = 10

    def set_memory(self, memory):
        self.memory = memory
        self.update()

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        total_height = self.height()
        width = self.width()

        used_memory = 0
        color_index = 0
        colors = [
            QtCore.Qt.red, QtCore.Qt.green, QtCore.Qt.blue,
            QtCore.Qt.cyan, QtCore.Qt.magenta, QtCore.Qt.yellow,
            QtCore.Qt.darkRed, QtCore.Qt.darkGreen, QtCore.Qt.darkBlue
        ]

        for app_name, size_mb in self.memory:
            height = (size_mb / (self.slot_size_mb * self.total_slots)) * total_height
            y = (used_memory / (self.slot_size_mb * self.total_slots)) * total_height

            rect = QtCore.QRectF(0, y, width, height)

            painter.fillRect(rect, colors[color_index % len(colors)])
            painter.drawRect(rect)
            painter.drawText(rect, QtCore.Qt.AlignCenter, f"{app_name} ({size_mb}MB)")

            used_memory += size_mb
            color_index += 1

class MemorySimulator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OS Memory Management Simulator")
        self.setGeometry(100, 100, 700, 500)

        self.total_slots = 10
        self.slot_size_mb = 20
        self.total_memory_mb = self.total_slots * self.slot_size_mb

        self.memory = deque()  # stores (app_name, size_mb)
        self.used_memory_mb = 0
        self.page_faults = 0
        self.app_history = []

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        self.app_name_input = QLineEdit()
        self.app_name_input.setPlaceholderText("Enter Application Name")

        self.memory_input = QLineEdit()
        self.memory_input.setPlaceholderText("Enter Memory (MB)")

        self.load_button = QPushButton("Load App")
        self.load_button.clicked.connect(self.load_app)

        self.defrag_button = QPushButton("Defragment Memory")
        self.defrag_button.clicked.connect(self.defragment_memory)

        self.algorithm_box = QComboBox()
        self.algorithm_box.addItems(["FIFO", "LRU"])

        input_layout.addWidget(self.app_name_input)
        input_layout.addWidget(self.memory_input)
        input_layout.addWidget(self.load_button)
        input_layout.addWidget(self.defrag_button)
        input_layout.addWidget(self.algorithm_box)

        layout.addLayout(input_layout)

        self.memory_canvas = MemoryCanvas()
        self.memory_canvas.setFixedHeight(300)
        layout.addWidget(self.memory_canvas)

        self.page_fault_label = QLabel("Page Faults: 0")
        layout.addWidget(self.page_fault_label)

        self.setLayout(layout)

    def load_app(self):
        name = self.app_name_input.text().strip()
        size_str = self.memory_input.text().strip()

        try:
            size = float(size_str)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Enter valid app name and numeric memory.")
            return

        if not name or size <= 0:
            QMessageBox.warning(self, "Invalid Input", "App name and size must be valid.")
            return

        if any(app[0] == name for app in self.memory):
            QMessageBox.information(self, "Already Loaded", f"{name} is already in memory.")
            return

        algo = self.algorithm_box.currentText()
        if algo == "FIFO":
            self.fifo_algorithm(name, size)
        elif algo == "LRU":
            self.lru_algorithm(name, size)

        self.app_name_input.clear()
        self.memory_input.clear()
        self.update_table()

    def fifo_algorithm(self, name, size):
        while self.used_memory_mb + size > self.total_memory_mb:
            if not self.memory:
                break
            removed_app = self.memory.popleft()
            self.used_memory_mb -= removed_app[1]
            print(f"Removed {removed_app[0]} ({removed_app[1]} MB)")

        self.memory.append((name, size))
        self.used_memory_mb += size
        self.page_faults += 1

    def lru_algorithm(self, name, size):
        while self.used_memory_mb + size > self.total_memory_mb:
            if not self.memory:
                break
            removed_app = self.memory.popleft()
            self.used_memory_mb -= removed_app[1]
            print(f"Removed {removed_app[0]} ({removed_app[1]} MB)")

        self.memory.append((name, size))
        self.used_memory_mb += size
        self.page_faults += 1

    def defragment_memory(self):
        seen = set()
        new_memory = deque()
        for app in reversed(self.memory):
            if app[0] not in seen:
                seen.add(app[0])
                new_memory.appendleft(app)
        self.memory = new_memory
        QMessageBox.information(self, "Defragmentation", "Memory defragmented!")
        self.update_table()

    def update_table(self):
        self.memory_canvas.set_memory(list(self.memory))
        self.page_fault_label.setText(f"Page Faults: {self.page_faults}")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MemorySimulator()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
