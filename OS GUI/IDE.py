from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
import tkinter.messagebox
from tkinter import messagebox
import subprocess
import os
from PIL import Image, ImageTk  # Import Pillow for image handling
import speech_recognition as sr
import threading
from tkinter import Tk, Button, Frame, Label
from tkinter.font import Font
import pyaudio
import wave
import cv2
import time
from calculator import CalculatorWidget
from camera import CameraViewer
from StartUp import StartUp
from tooltip import create_tooltip
from iconpaths import icon
from resize import resize_icon
from toolbar import ToolbarTop
from voice_commands import VoiceController
from taskbar import Taskbar
from desktop import Desktop
import app_callbacks as apps
from voicewidget import VoiceAssistantWidget

honeyBoot = StartUp(
        path="OS GUI/assets/Final.mp4",  # Adjust path if needed
        window_size=(780, 518),
        duration=2,
        fullscreen=False  # or True if you prefer fullscreen
    )
honeyBoot.play()


Honey_screen = Tk()
Honey_screen.title('Ikiyo')
camera_viewer = CameraViewer(Honey_screen)
background_image_path = 'OS GUI/assets/background2.png'
Honey_screen_width = Honey_screen.winfo_screenwidth()
Honey_screen_height = Honey_screen.winfo_screenheight()

# Create the Notebook widget as part of the main set up
# notebook = ttk.Notebook(Honey_screen)
# notebook.pack(side='left', fill='both', expand=True)

#Setting up the background Image
bg_image = Image.open(background_image_path)
bg_image = bg_image.resize((Honey_screen_width, Honey_screen_height), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

background_label = Label(Honey_screen, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.image = bg_photo  #keep a reference



editor = None
calculator = None
is_dark_mode = False
####################################################################

#Create a custom font
custom_font = Font(family="Helvetica", size=10, weight="normal")

#Create a Frame that will hold Label
background_frame = Frame(Honey_screen, bg="#454543")
background_frame.pack(fill="x", side="top", anchor="ne")

#Creating a Label Widget
HoneyLabel = Label(background_frame, text="Honey OS", font=custom_font, bg="#454543", fg="#FFFFFF")
#Shoving it into the Screen
HoneyLabel.pack()


isEditorActive = 0
isCalculatorActive = 0
if isEditorActive == 1:
  editor = Text(Honey_screen, undo=True, relief=FLAT)
  editor.pack(side=LEFT, fill=BOTH, expand=False, padx=10, pady=20)
  editor.bind('<Key>', check_text_and_toggle_buttons)

if isCalculatorActive == 1:
  calculator = CalculatorWidget(Honey_screen)
  calculator.pack(side=RIGHT, fill=BOTH, expand=False, padx=10, pady=20)

############################################################################################
######                         PATH AND ICONS                         ######
############################################################################################

icon_sizes = {
    "new_file": (30, 30),
    "open_file": (30, 30),
    "microphone": (30, 30),
    "mic_listen": (30, 30),
    "open_microphone": (130, 130),
    "save": (30, 30),
    "save_as": (30, 30),
    "copy": (30, 30),
    "paste": (30, 30),
    "camera": (30, 30),
    "cut": (30, 30),
    "undo": (30, 30),
    "redo": (30, 30),
    "calculator": (30, 30),
    "close": (15, 15),
    "minimize": (15, 15)
}

icons = {
    key: resize_icon(icon[key], size=icon_sizes.get(key, (30, 30)))
    for key in icon
}

############################################################################################
######                         Button Functions                         ######
############################################################################################

# Open new file
def open_new_file():
  global file_path
  global unsaved_changes
  
  # editor = create_tab(title= 'Untitled')
  editor.delete('1.0', END)
  file_path = ''
  Honey_screen.title('Bluefire - New File')

  display_voice_command_feedback(file_path)
  unsaved_changes = False


# Opens an existing file
def open_existing_file():
  global file_path
  global unsaved_changes

  code = editor.get('1.0', END).strip()

  if code:
    tkinter.messagebox.showerror("Unable to Save", "Do you want to save changes?")
  path = askopenfilename(filetypes=[('Bluefire Files', '*.blu')])
  if path:
    with open(path, 'r') as file:
      code = file.read()

      editor.delete('1.0', END)
      # editor = create_tab(content=code, title=os.path.basename(path))

      editor.insert('1.0', code)
      set_file_path(path)
      Honey_screen.title(f'Bluefire - {os.path.basename(path)}')

      display_voice_command_feedback(path)
  unsaved_changes = False


# This function is to save the content of the editor
def save():
  global file_path
  global unsaved_changes

  code = editor.get('1.0', END).strip()
  if code:
    # toggle_button_state(save_btn, DISABLED)
    tkinter.messagebox.showerror("Unable to Save", "Do you want to save changes?")
    return
  if not file_path:
    path = asksaveasfilename(filetypes=[('Bluefire Files', '*.blu')])
  else:
    path = file_path
  if not path:
    return
  if not path.endswith('.blu'):
    path += '.blu'
  with open(path, 'w') as file:
    file.write(code)
    set_file_path(path)
  unsaved_changes = False


# This function saves the content of the editor to a new file
def save_as():
  global unsaved_changes

  code = editor.get('1.0', END).strip()
  if not code:
    tkinter.messagebox.showerror("Unable to Save", "There is no content to save.")
    return
  path = asksaveasfilename(filetypes=[('Bluefire Files', '*.blu')])
  if not path:
    return
  if not path.endswith('.blu'):
    path += '.blu'
  with open(path, 'w') as file:
    file.write(code)
    set_file_path(path)
  unsaved_changes = False


def toggleEditor():
    global isEditorActive
    global editor
    
    if isEditorActive == 1:
      isEditorActive = 0
    else:
      isEditorActive = 1
      
    if isEditorActive == 1:
        editor = Text(Honey_screen, undo=True, relief=FLAT)
        editor.pack(side=LEFT, fill=BOTH, expand=False, padx=10, pady=20)
        editor.bind('<Key>', check_text_and_toggle_buttons)
    else:
        editor.destroy()  # removes the widget completely

def toggleCalculator():
    global isCalculatorActive, calculator

    if isCalculatorActive:
        calculator.destroy()
        isCalculatorActive = False
        calculator = None
    else:
        calculator = tk.Toplevel(Honey_screen)  # Floating window
        calculator.overrideredirect(True)       # Remove title bar for custom dragging
        calculator.geometry("250x300+100+100")  # Initial size and position

        widget = CalculatorWidget(calculator)
        widget.pack(fill=tk.BOTH, expand=True)

        # Bind mouse events to make it draggable
        def start_move(event):
            calculator.x = event.x
            calculator.y = event.y

        def do_move(event):
            x = calculator.winfo_x() + event.x - calculator.x
            y = calculator.winfo_y() + event.y - calculator.y
            calculator.geometry(f"+{x}+{y}")

        calculator.bind("<Button-1>", start_move)
        calculator.bind("<B1-Motion>", do_move)
        isCalculatorActive = True

  

def cut_text():
  editor.event_generate("<<Cut>>")


def copy_text():
  editor.event_generate("<<Copy>>")


def paste_text():
  editor.event_generate("<<Paste>>")


def undo_text():
  editor.edit_undo()


def redo_text():
  editor.edit_redo()

  
def close_window():
  # global file_path
  if isEditorActive == 1:
    code = editor.get('1.0', END).strip()
    if code:
      tkinter.messagebox.showerror("Unable to Save", "Do you want to save changes?")
      save()
      Honey_screen.destroy()
  Honey_screen.destroy()


def minimize_window():
  Honey_screen.iconify()


############################################################################################
######                                                               ######
############################################################################################


# This is a toggle for the light and dark theme
def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode  # Toggle the theme flag

    # Determine the current theme based on the is_dark_mode flag
    theme = dark_theme if is_dark_mode else light_theme

    # Update main window background
    if Honey_screen is not None:
        Honey_screen.config(bg=theme["bg"])

    # Update editor if exists and not None
    if 'editor' in globals() and editor is not None:
        editor.config(bg=theme["editor_bg"], fg=theme["editor_fg"], insertbackground=theme["fg"])

    # Update toolbar and its children (buttons)
    if toolbar is not None:
        toolbar.config(bg=theme["toolbar_bg"])
        for widget in toolbar.winfo_children():
            widget.config(bg=theme["button_bg"], activebackground=theme["button_bg"], fg=theme["fg"])

    # Update voice command feedback if exists and not None
    if 'voice_command_feedback' in globals() and voice_command_feedback is not None:
        voice_command_feedback.config(bg=theme["output_bg"], fg=theme["output_fg"])

toolbar = ToolbarTop(
    Honey_screen,
    icons=icons,
    callbacks={
        "open_new_file": open_new_file,
        "open_existing_file": open_existing_file,
        "save": save,
        "save_as": save_as,
        "copy": copy_text,
        "paste": paste_text,
        "cut": cut_text,
        "undo": undo_text,
        "redo": redo_text,
        "close_window": close_window,
        "minimize_window": minimize_window,
        "toggle_theme": toggle_theme,
        "activate_commands": lambda: None,  # Temporary placeholder
        "toggleEditor": toggleEditor,
        "toggleCalculator": toggleCalculator,
        "open_camera": camera_viewer.open_camera
    },
    create_tooltip=create_tooltip
)
toolbar.pack(side="top", fill="x")

desktop = Desktop(Honey_screen, grid_size=75)
desktop.pack(fill="both", expand=True)



desktop.add_icon("Editor", "OS GUI/assets/cross.png", apps.open_editor, (0, 0))
desktop.add_icon("Calculator", "OS GUI/assets/cross.png", apps.open_calculator, (100, 0))
desktop.add_icon("Files", "OS GUI/assets/cross.png", apps.open_files, (0, 100))


voice_widget = VoiceAssistantWidget(desktop, font_size=12, button_command=lambda: None,mic_icon=icons["mic"])
desktop.add_widget(voice_widget, width=600, height=80)
voice_widget.show_feedback("Say 'Honey' to activate commands...")

# Step 2: Now create voice_controller with toolbar available
voice_controller = VoiceController(
    toolbar=toolbar,
    icons=icons,
    mic_icon=icons["microphone"],
    mic_listening_icon=icons["mic_listen"],
    display_feedback=voice_widget.show_feedback,
    calculator=calculator,
    editor=editor,
    is_calculator_active=isCalculatorActive,
    is_dark_mode=is_dark_mode
)
voice_widget.action_button.config(command=voice_controller.activate_commands)

voice_controller.start_listening()

# Step 3: Update the command binding now that voice_controller exists
toolbar.commands["activate_commands"] = voice_controller.activate_commands

taskbar = Taskbar(Honey_screen, apps=[])
taskbar.pack(side="bottom", fill="x")

############################################################################################
######                              DICTIONARY                          ######
############################################################################################

light_theme = {
    "bg": "#FFFFFF",
    "fg": "#000000",
    "button_bg": "#fcfcd7",
    "editor_bg": "#FFFFFF",
    "editor_fg": "#000000",
    "toolbar_bg": "#fcfcd7",
    "output_bg": "#AD7D02",
    "output_fg": "#000000",
}

dark_theme = {
    "bg": "#252620",
    "fg": "#f8f8f2",
    "button_bg": "#30302d",
    "editor_bg": "#3b3b38",
    "editor_fg": "#f8f8f2",
    "toolbar_bg": "#30302d",
    "output_bg": "#30302d",
    "output_fg": "#f8f8f2",
}

############################################################################################
######                                                               ######
############################################################################################

# A flag to help keep track of the buttons
unsaved_changes = False

def set_file_path(path):
  global file_path
  file_path = path

# Enables the button once it notice text in the editor
def check_text_and_toggle_buttons(event=None):
  global unsaved_changes
  content = editor.get("1.0", END).strip()
  if content:
    unsaved_changes = True
  else:
    unsaved_changes = False

screen_height = Honey_screen.winfo_screenheight()


# Optionally bind to button
toolbar.mic_btn.config(command=voice_controller.activate_commands)


Honey_screen.attributes('-fullscreen', True)
# Honey_screen.config(bg='#FFCF81')

# Honey_screen.overrideredirect(True)  # This removes the window decorations
Honey_screen.mainloop()
