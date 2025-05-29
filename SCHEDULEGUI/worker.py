from PyQt5.QtCore import QThread, pyqtSignal


class WorkerThread(QThread):
    update_gui_signal = pyqtSignal(list)

    def __init__(self, num_processes, mode="sjf"):
        super().__init__()
        self.num_processes = num_processes
        self.mode = mode

    def run(self):
        from main import main
        main(self.num_processes, update_gui_signal=self.update_gui_signal.emit, mode=self.mode)
