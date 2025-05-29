from tkinter import *
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

honeyBoot = StartUp(
        path="OS GUI/assets/Final.mp4",  # Adjust path if needed
        window_size=(780, 518),
        duration=2,
        fullscreen=False  # or True if you prefer fullscreen
    )
honeyBoot.play()


Honey_screen = Tk()
Honey_screen.title('Bluefire IDE')
file_path = ''
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
  enable_buttons(NORMAL)


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
        calculator = CalculatorWidget(Honey_screen)
        calculator.pack(side=RIGHT, fill=BOTH, expand=False, padx=10, pady=20)
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


# def maximize_window():
#     Honey_screen.state('zoomed')



def display_voice_command_feedback(text):
  # Clear previous feedback
  voice_command_feedback.config(state=NORMAL)
  voice_command_feedback.delete('1.0', END)

  # Display new feedback
  voice_command_feedback.insert('1.0', text)
  voice_command_feedback.config(state=DISABLED)

#################### COPIED FUNCTIONS #############################
#Microphone Activate Commands

def stop_listening():
    global listening
    listening = False

def activate_commands():
    # Start listening for commands in a separate thread
    threading.Thread(target=voice_commands, daemon=True).start()

    toolbar.mic_btn.config(image=icons["mic_listen"])
    toolbar.mic_btn.image = icons["mic_listen"]
    display_voice_command_feedback("I'm here, dear. What can I do for you?")

    # After a short delay, return the mic button to normal state
    restore_mic_icon()


############################################################################################
######                                                               ######
############################################################################################


# This is a toggle for the light and dark theme
def toggle_theme():
  global is_dark_mode
  is_dark_mode = not is_dark_mode  #Toggle the theme flag

  #Determine the current theme based on the is_dark_mode flag
  theme = dark_theme if is_dark_mode else light_theme

  # Update main window background
  Honey_screen.config(bg=theme["bg"])

  # Update editor
  if 'editor' in globals():
    editor.config(bg=theme["editor_bg"], fg=theme["editor_fg"], insertbackground=theme["fg"])

  # Update toolbar and its children (buttons)
  toolbar.config(bg=theme["toolbar_bg"])
  for widget in toolbar.winfo_children():
    widget.config(bg=theme["button_bg"], activebackground=theme["button_bg"], fg=theme["fg"])

  # Update voice command feedback and code output
  voice_command_feedback.config(bg=theme["output_bg"], fg=theme["output_fg"])

  #Update the Theme button text color
  # toggle_theme_btn.config(fg=theme["fg"]) #Changes the text color

toolbar = ToolbarTop(
    Honey_screen,  # parent window/frame
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
        "activate_commands": activate_commands,
        "toggleEditor": toggleEditor,
        "toggleCalculator": toggleCalculator,
        "open_camera": camera_viewer.open_camera
    },
    create_tooltip=create_tooltip
)
toolbar.pack(side="top", fill="x")




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

#light mode default
is_dark_mode = False

def set_file_path(path):
  global file_path
  file_path = path


############################################################################################
######                                                               ######
############################################################################################
def listen_for_commands():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("Say 'Honey' to activate commands...")
    while True:
      print("Test")
      try:
        audio_data = r.listen(source)
        text = r.recognize_google(audio_data).lower()
        if "honey" in text:
          print("Honey Test")
          toolbar.mic_btn.config(image=mic_listening_icon)
          toolbar.mic_btn.image = mic_listening_icon
          display_voice_command_feedback("Yes, dear?")
          voice_commands()  # Call the command processing function
          stop_listening()
          toolbar.mic_btn.config(image=mic_icon)
          toolbar.mic_btn.image = mic_icon
        
    
      except sr.UnknownValueError:
        pass
      except sr.RequestError as e:
        print(f"Sorry, dear. I unfortunately can't do that... ({e})")


def restore_mic_icon():
    toolbar.mic_btn.config(image=mic_icon)
    toolbar.mic_btn.image = mic_icon


def activate_commands():
    # Start listening for commands in a separate thread
    threading.Thread(target=voice_commands, daemon=True).start()
    
    toolbar.mic_btn.config(image=mic_listening_icon)
    toolbar.mic_btn.image = mic_listening_icon
    
    display_voice_command_feedback("I'm here, dear. What can I do for you?")



def voice_commands():
  global listening
  global is_dark_mode
  r = sr.Recognizer()
  with sr.Microphone() as source:
    try:
      audio_data = r.listen(source, timeout=5)
      command_text = r.recognize_google(audio_data).lower()
      display_voice_command_feedback(
          f"Okay, dear. Let me quickly do that for you... ({command_text})")
      
      if isCalculatorActive == 1:
          if "calculator" in command_text:
              toolbar.commands["toggle_calculator"]()
          else:
              calculator.set_input_from_string(command_text)
      elif "new file please" in command_text:
          toolbar.commands["new_file"]()
      elif "existing file please" in command_text or "abrihi" in command_text:
          toolbar.commands["open_file"]()
      elif "save please" in command_text:
          toolbar.commands["save"]()
      elif "save as please" in command_text or "save us please" in command_text:
          toolbar.commands["save_as"]()
      elif "copy please" in command_text:
          toolbar.commands["copy"]()
      elif "cut please" in command_text:
          toolbar.commands["cut"]()
      elif "paste please" in command_text:
          toolbar.commands["paste"]()
      elif "undo please" in command_text:
          toolbar.commands["undo"]()
      elif "redo please" in command_text:
          toolbar.commands["redo"]()
      elif "dark mode please" in command_text or "dark" in command_text:
          if not is_dark_mode:
              toolbar.commands["toggle_theme"]()
      elif "light mode please" in command_text or "open the curtains please" in command_text:
          if is_dark_mode:
              toolbar.commands["toggle_theme"]()
      elif "minimize please" in command_text:
          toolbar.commands["minimize"]()
      elif command_text in ["exit please", "shut up", "avada kedavra", "yamete"]:
          toolbar.commands["close"]()
      elif "editor" in command_text:
          toolbar.commands["toggle_editor"]()
      elif "calculator" in command_text:
          toolbar.commands["toggle_calculator"]()
      

    except Exception as e:
      display_voice_command_feedback(
          f"Sorry, dear. I didn't quite get that... ({str(e)})")
    
    stop_listening()
    restore_mic_icon()


############################################################################################
######                                                               ######
############################################################################################


def start_listening():
  toolbar.mic_btn.config()
  threading.Thread(target=listen_for_commands, daemon=True).start()


# Enables the button once it notice text in the editor
def check_text_and_toggle_buttons(event=None):
  global unsaved_changes
  content = editor.get("1.0", END).strip()
  if content:
    unsaved_changes = True
  else:
    unsaved_changes = False




############################################################################################
######                      TOOLBAR  |  BUTTONS                       ######
############################################################################################


# Voice command feedback area
voice_command_feedback = Text(Honey_screen, height=3, font = Font(family="Courier New", size=20, weight="bold"), state=DISABLED, bg=light_theme["output_bg"], fg=light_theme["output_fg"])
voice_command_feedback.pack(side=BOTTOM, fill=X)
voice_command_feedback.config()

screen_height = Honey_screen.winfo_screenheight()

isEditorActive = 0
isCalculatorActive = 0
if isEditorActive == 1:
  global editor
  editor = Text(Honey_screen, undo=True, relief=FLAT)
  editor.pack(side=LEFT, fill=BOTH, expand=False, padx=10, pady=20)
  editor.bind('<Key>', check_text_and_toggle_buttons)

if isCalculatorActive == 1:
  calculator = CalculatorWidget(Honey_screen)
  calculator.pack(side=RIGHT, fill=BOTH, expand=False, padx=10, pady=20)



start_listening()

Honey_screen.attributes('-fullscreen', True)
# Honey_screen.config(bg='#FFCF81')

# Honey_screen.overrideredirect(True)  # This removes the window decorations
Honey_screen.mainloop()
