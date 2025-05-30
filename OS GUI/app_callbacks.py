
import subprocess
import os
import sys
import tkinter as tk
from calculator import CalculatorWidget  # Adjust if you named it differently
from camera import CameraViewer
Honey_screen = None  # You will assign this from your main IDE
def set_main_screen(screen):
    """Call this from IDE.py to inject the main window reference."""
    global Honey_screen
    global camera_viewer
    Honey_screen = screen
    camera_viewer = CameraViewer(Honey_screen)


def open_editor():
    print("Editor opened!")

camera_instance = None

def open_camera():
    global camera_instance
    if camera_instance is None or not camera_instance.running:
        camera_instance = CameraViewer(Honey_screen)
        camera_instance.open_camera()

def take_picture():
    global camera_instance
    print("reached not)")
    if camera_instance is not None and camera_instance.running:
        print("reached)")
        camera_instance.take_picture()
    else:
        print("Camera is not running, cannot take picture.")

def close_camera():
    global camera_instance
    if camera_instance is not None and camera_instance.running:
        camera_instance.close_camera()
        camera_instance = None


# Globals (you can also use a better state manager if desired)
isCalculatorActive = False
calculator = None
Honey_screen = None  # You will assign this from your main IDE
simulator_process = None  # To track the launched process


def open_calculator():
    global isCalculatorActive, calculator, Honey_screen

    if isCalculatorActive:
        return  # Do nothing if already open

    calculator = tk.Toplevel(Honey_screen)
    calculator.overrideredirect(True)
    calculator.geometry("250x300+100+100")

    # === Header Frame ===
    header = tk.Frame(calculator, bg="gray20")
    header.pack(fill="x")

    # Title Label
    title = tk.Label(header, text="Calculator", fg="white", bg="gray20", font=("Arial", 10, "bold"))
    title.pack(side="left", padx=5)

    # Close Button
    def on_close():
        global isCalculatorActive, calculator
        isCalculatorActive = False
        calculator.destroy()
        calculator = None

    close_button = tk.Button(
        header, text="✖", command=on_close,
        bg="red", fg="white", font=("Arial", 10, "bold"),
        bd=0, cursor="hand2"
    )
    close_button.pack(side="right", padx=5, pady=2)

    # === Make Window Draggable by Header ===
    def start_move(event):
        calculator.x = event.x
        calculator.y = event.y

    def do_move(event):
        x = calculator.winfo_x() + event.x - calculator.x
        y = calculator.winfo_y() + event.y - calculator.y
        calculator.geometry(f"+{x}+{y}")

    header.bind("<ButtonPress-1>", start_move)
    header.bind("<B1-Motion>", do_move)

    # === Calculator Content ===
    widget = CalculatorWidget(calculator)
    widget.pack(fill=tk.BOTH, expand=True)

    isCalculatorActive = True

def shutdown():
    Honey_screen.destroy()

def close_calculator():
    global isCalculatorActive, calculator
    if calculator is not None:
        calculator.destroy()
        calculator = None
        isCalculatorActive = False

def close_calculator():
    global isCalculatorActive, calculator
    if calculator is not None:
        calculator.destroy()
        calculator = None
        isCalculatorActive = False


def open_simulator():
    global simulator_process
    simulator_path = os.path.join(os.path.dirname(__file__), '..', 'SCHEDULEGUI', 'PCB_scheduler_final.py')
    simulator_path = os.path.abspath(simulator_path)
    simulator_process = subprocess.Popen([sys.executable, simulator_path])

def close_simulator():
    global simulator_process
    if simulator_process and simulator_process.poll() is None:
        simulator_process.terminate()
        simulator_process = None
        print("Simulator closed.")
    else:
        print("No simulator is running.")


def set_main_screen(screen):
    """Call this from IDE.py to inject the main window reference."""
    global Honey_screen
    Honey_screen = screen

def open_files():
    print("Files opened!")
