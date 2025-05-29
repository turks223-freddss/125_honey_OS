# bluefire_ide/runner.py

import subprocess
import tkinter as tk
from .file_state import get_file_path

def run(output_widget):
    path = get_file_path()
    if not path:
        popup = tk.Toplevel()
        tk.Label(popup, text="Please save your code first!").pack()
        return

    command = f'python "{path}"'
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    output, error = process.communicate()
    output_widget.delete('1.0', 'end')
    output_widget.insert('end', error.decode() + output.decode())
