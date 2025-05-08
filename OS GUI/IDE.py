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


def play_video(path, window_size):
  cap = cv2.VideoCapture(path)

  if not cap.isOpened():
    print("Error: Could not open video.")
    return

  cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

  cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

  # Resize the window to the specified size
  cv2.resizeWindow('Video', window_size[0], window_size[1])

  # Use tkinter to get the screen size
  root = tkinter.Tk()
  screen_width = root.winfo_screenwidth()
  screen_height = root.winfo_screenheight()
  root.destroy()

  # Calculate the position to center the window
  x_position = (screen_width - window_size[0]) // 2
  y_position = ((screen_height - window_size[1]) // 2) + (-10)

  # Move the window to the center of the screen
  cv2.moveWindow('Video', x_position, y_position)

  start_time = time.time()  # Capture the start time

  while True:
    ret, frame = cap.read()
    if not ret:
      print("Reached end of video or error occurred. Exiting.")
      break

    frame = cv2.resize(frame, window_size, interpolation=cv2.INTER_AREA)
    cv2.imshow('Video', frame)

    # Check if 14 seconds have passed
    if time.time() - start_time > 1:
      break

    if cv2.waitKey(15) & 0xFF == ord('q') or cv2.getWindowProperty(
        'Video', cv2.WND_PROP_VISIBLE) < 1:
      break

  cap.release()
  cv2.destroyAllWindows()


# Declare the window size before calling the function
window_size = (780, 518)  # Width, Height
video_path = 'OS GUI/assets/Final.mp4'
play_video(video_path, window_size)

Honey_screen = Tk()
Honey_screen.title('Bluefire IDE')
file_path = ''

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


#################### COPIED FUNCTIONS #############################
#Microphone Activate Commands

def stop_listening():
    global listening
    listening = False

def activate_commands():
    # Start listening for commands in a separate thread
    threading.Thread(target=voice_commands, daemon=True).start()

    mic_btn.config(image=mic_listening_icon)
    mic_btn.image = mic_listening_icon
    display_voice_command_feedback("I'm here, dear. What can I do for you?")

    # After a short delay, return the mic button to normal state
    restore_mic_icon()


#Resize Icon
def resize_icon(path, size=(32, 32)):
  img = Image.open(path)
  img = img.resize(size, Image.Resampling.LANCZOS)
  return ImageTk.PhotoImage(img)


open_microp_path = 'OS GUI/assets/microphone.png'
open_microp_icon = resize_icon(open_microp_path, size=(130, 130))


#ToolTip
class ToolTip(object):

  def __init__(self, widget):
    self.widget = widget
    self.tipwindow = None
    self.x = self.y = 0
    self.text = None  # Add a text attribute to store the tooltip text

  def showtip(self, text):
    """Display text in tooltip window"""
    self.text = text  # Store the text to be displayed in the tooltip
    if self.tipwindow or not self.text:
      return

    self.tipwindow = tw = Toplevel(self.widget)
    x, y, cx, cy = self.widget.bbox("insert")
    x = x + self.widget.winfo_rootx()  # Adjust the x-coordinate as needed
    # Position below the widget: start at the widget's bottom-left corner
    y = y + self.widget.winfo_rooty() + self.widget.winfo_height()

    tw.wm_overrideredirect(True)
    tw.wm_geometry("+%d+%d" % (x, y))
    label = Label(
        tw,
        text=self.text,
        justify=LEFT,  # Use self.text here
        background="#ffffe0",
        relief=SOLID,
        borderwidth=1,
        font=("tahpma", "10", "normal"))
    label.pack(ipadx=1)

  def hidetip(self):
    if self.tipwindow:
      self.tipwindow.destroy()
      self.tipwindow = None


#Create ToolTip
def createToolTip(widget, text):
  toolTip = ToolTip(widget)

  def enter(event):
    toolTip.showtip(text)

  def leave(event):
    toolTip.hidetip()

  widget.bind('<Enter>', enter)
  widget.bind('<Leave>', leave)


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


def resize_icon(path, size=(32, 32)):
  img = Image.open(path)
  img = img.resize(size, Image.Resampling.LANCZOS)
  return ImageTk.PhotoImage(img)


# Adjust these paths to your actual icon paths
############################################################################################
######                         PATH AND ICONS                         ######
############################################################################################
new_file_icon_path = 'OS GUI/assets/new_file.png'
open_file_icon_path = 'OS GUI/assets/existing_file.png'
open_microp_path = 'OS GUI/assets/microphone.png'
save_path = 'OS GUI/assets/save.png'
save_as_path = 'OS GUI/assets/save_as.png'
copy_icon_path = 'OS GUI/assets/copy.png'
paste_path = 'OS GUI/assets/clipboard.png'
cut_path = 'OS GUI/assets/scissors.png'
undo_path = 'OS GUI/assets/refresh.png'
redo_path = 'OS GUI/assets/redo.png'
microphone_path = 'OS GUI/assets/mic.png'
close_path = 'OS GUI/assets/cross.png'
minimize_path = 'OS GUI/assets/minimize.png'
# maximize_path = 'OS GUI/assets/maximize.png'
background_image_path = 'OS GUI/assets/background.png'
mic_listen_path = 'OS GUI/assets/mic_listen.png'

new_file_icon = resize_icon(new_file_icon_path, size=(30, 30))
open_file_icon = resize_icon(open_file_icon_path, size=(30, 30))
mic_icon = resize_icon(microphone_path, size=(30, 30))
mic_listening_icon = resize_icon(mic_listen_path, size = (30, 30))
open_microp_icon = resize_icon(open_microp_path, size=(130, 130))
save_icon = resize_icon(save_path, size=(30, 30))
save_as_icon = resize_icon(save_as_path, size=(30, 30))
copy_icon = resize_icon(copy_icon_path, size=(30, 30))
paste_icon = resize_icon(paste_path, size=(30, 30))
cut_icon = resize_icon(cut_path, size=(30, 30))
undo_icon = resize_icon(undo_path, size=(30, 30))
redo_icon = resize_icon(redo_path, size=(30, 30))
close_icon = resize_icon(close_path, size=(15, 15))
minimize_icon = resize_icon(minimize_path, size=(15, 15))
# maximize_icon = resize_icon(maximize_path, size=(15, 15))

############################################################################################
######                                                               ######
############################################################################################


def close_window():
  # global file_path

  code = editor.get('1.0', END).strip()
  if code:
    tkinter.messagebox.showerror("Unable to Save", "Do you want to save changes?")
    save()
  Honey_screen.destroy()


def minimize_window():
  Honey_screen.iconify()


# def maximize_window():
#     Honey_screen.state('zoomed')


class ToolTip(object):

  def __init__(self, widget):
    self.widget = widget
    self.tipwindow = None
    self.x = self.y = 0
    self.text = None  # Add a text attribute to store the tooltip text

  def showtip(self, text):
    """Display text in tooltip window"""
    self.text = text  # Store the text to be displayed in the tooltip
    if self.tipwindow or not self.text:
      return

    self.tipwindow = tw = Toplevel(self.widget)
    x, y, cx, cy = self.widget.bbox("insert")
    x = x + self.widget.winfo_rootx()  # Adjust the x-coordinate as needed
    # Position below the widget: start at the widget's bottom-left corner
    y = y + self.widget.winfo_rooty() + self.widget.winfo_height()

    tw.wm_overrideredirect(True)
    tw.wm_geometry("+%d+%d" % (x, y))
    label = Label(
        tw,
        text=self.text,
        justify=LEFT,  # Use self.text here
        background="#ffffe0",
        relief=SOLID,
        borderwidth=1,
        font=("tahpma", "10", "normal"))
    label.pack(ipadx=1)

  def hidetip(self):
    if self.tipwindow:
      self.tipwindow.destroy()
      self.tipwindow = None


def createToolTip(widget, text):
  toolTip = ToolTip(widget)

  def enter(event):
    toolTip.showtip(text)

  def leave(event):
    toolTip.hidetip()

  widget.bind('<Enter>', enter)
  widget.bind('<Leave>', leave)


def display_voice_command_feedback(text):
  # Clear previous feedback
  voice_command_feedback.config(state=NORMAL)
  voice_command_feedback.delete('1.0', END)

  # Display new feedback
  voice_command_feedback.insert('1.0', text)
  voice_command_feedback.config(state=DISABLED)


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
          mic_btn.config(image=mic_listening_icon)
          mic_btn.image = mic_listening_icon
          display_voice_command_feedback("Yes, dear?")
          voice_commands()  # Call the command processing function
          stop_listening()
          mic_btn.config(image=mic_icon)
          mic_btn.image = mic_icon
        
    
      except sr.UnknownValueError:
        pass
      except sr.RequestError as e:
        print(f"Sorry, dear. I unfortunately can't do that... ({e})")


def restore_mic_icon():
    mic_btn.config(image=mic_icon)
    mic_btn.image = mic_icon


def activate_commands():
    # Start listening for commands in a separate thread
    threading.Thread(target=voice_commands, daemon=True).start()
    
    mic_btn.config(image=mic_listening_icon)
    mic_btn.image = mic_listening_icon
    
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

      ############################################################################################
      ######                         VOICE COMMANDS                         ######
      ############################################################################################

      # open a new file
      if "new file please" in command_text.lower():
        open_new_file()
      # open an existing file
      elif "existing file please" in command_text.lower():
        open_existing_file()
      elif "abrihi" in command_text.lower():
        open_existing_file()
      # save file
      elif "save please" in command_text.lower():
        save()
      #save as
      elif "save as please" in command_text.lower():
        save_as()
      elif "save us please" in command_text.lower():
        save_as()
      # copy text
      elif "copy please" in command_text.lower():
        copy_text()
      # cut text
      elif "cut please" in command_text.lower():
        cut_text()
      # paste text
      elif "paste please" in command_text.lower():
        paste_text()
      # undo text
      elif "undo please" in command_text.lower():
        undo_text()
      # redo text
      elif "redo please" in command_text.lower():
        redo_text()
      # change theme to dark mode
      elif "dark mode please" in command_text.lower():
        if not is_dark_mode:
          toggle_theme()
      elif "dark" in command_text.lower():
        if not is_dark_mode:
          toggle_theme()
      # change theme to light mode
      elif "light mode please" in command_text.lower():
        if is_dark_mode:
          toggle_theme()
      elif "open the curtains please" in command_text.lower():
        if is_dark_mode:
          toggle_theme()
      # minimize window
      elif "minimize please" in command_text.lower():
        minimize_window()
      # close window
      elif "exit please" in command_text.lower():
        close_window()
      elif "shut up" in command_text.lower():
        close_window()
      elif "avada kedavra" in command_text.lower():
        close_window()
      elif"yamete" in command_text.lower():
        close_window()

    except Exception as e:
      display_voice_command_feedback(
          f"Sorry, dear. I didn't quite get that... ({str(e)})")
    
    stop_listening()
    restore_mic_icon()


############################################################################################
######                                                               ######
############################################################################################


def start_listening():
  mic_btn.config()
  threading.Thread(target=listen_for_commands, daemon=True).start()


# Enables the button once it notice text in the editor
def check_text_and_toggle_buttons(event=None):
  global unsaved_changes
  content = editor.get("1.0", END).strip()
  if content:
    unsaved_changes = True
    disabled_buttons(NORMAL)
    enable_buttons(NORMAL)
  else:
    unsaved_changes = False
    enable_buttons(DISABLED)


############################################################################################
######                         Button Functions                         ######
############################################################################################

# def create_tab(content=None, title='New Tab'):
# #   Create a new tab with a text widget inside it
#     new_tab = ttk.Frame(notebook)
#     notebook.add(new_tab, text=title)
#     # text_widget = Text(new_tab, undo=True, relief=FLAT)
#     editor.pack(side='left', fill='both', expand=True)
#     if content:
#       editor.insert('end', content)
      
#     return editor

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
  disabled_buttons(DISABLED)


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
  disabled_buttons(DISABLED)


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


def hide_editor(event=None):
  editor.pack_forget()  # This hides the editor widget


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


# This function disables of the buttons
def disabled_buttons(state):
  save_btn.config(state=state)
  undo_btn.config(state=state)
  redo_btn.config(state=state)


def enable_buttons(state):
  save_as_btn.config(state=state)
  copy_btn.config(state=state)
  paste_btn.config(state=state)
  cut_btn.config(state=state)


############################################################################################
######                      TOOLBAR  |  BUTTONS                       ######
############################################################################################


def create_toolbar_top():
  global toolbar
  toolbar = Frame(Honey_screen, relief=FLAT)



  # New File Button
  new_file_btn = Button(toolbar, image=new_file_icon, command=open_new_file, relief=FLAT)
  new_file_btn.image = new_file_icon
  new_file_btn.pack(side=LEFT, padx=2, pady=2)
  createToolTip(new_file_btn, "New File")

  # Open Existing File Button
  open_file_btn = Button(toolbar, image=open_file_icon, command=open_existing_file, relief=FLAT)
  open_file_btn.image = open_file_icon
  open_file_btn.pack(side=LEFT, padx=2, pady=2)
  createToolTip(open_file_btn, "Existing File")

  # Save Button
  global save_btn
  save_btn = Button(toolbar, image=save_icon, command=save, relief=FLAT)
  save_btn.image = save_icon
  save_btn.pack(side=LEFT, padx=2, pady=2)
  createToolTip(save_btn, "Save")

  # Save As Button
  global save_as_btn
  save_as_btn = Button(toolbar,image=save_as_icon,command=save_as,relief=FLAT)
  save_as_btn.image = save_as_icon
  save_as_btn.pack(side=LEFT, padx=2, pady=2)
  createToolTip(save_as_btn, "Save As")

  # Copy Button
  global copy_btn
  copy_btn = Button(toolbar, image=copy_icon, command=copy_text, relief=FLAT)
  copy_btn.image = copy_icon
  copy_btn.pack(side=LEFT, padx=2, pady=2)
  createToolTip(copy_btn, "Copy")

  # Paste Button
  global paste_btn
  paste_btn = Button(toolbar, image=paste_icon, command=paste_text, relief=FLAT)
  paste_btn.image = paste_icon
  paste_btn.pack(side=LEFT, padx=2, pady=2)
  createToolTip(paste_btn, "Paste")

  # Cut Button
  global cut_btn
  cut_btn = Button(toolbar, image=cut_icon, command=cut_text, relief=FLAT)
  cut_btn.image = cut_icon
  cut_btn.pack(side=LEFT, padx=2, pady=2)
  createToolTip(cut_btn, "Cut")

  # Undo Button
  global undo_btn
  undo_btn = Button(toolbar, image=redo_icon, command=undo_text, relief=FLAT)
  undo_btn.image = redo_icon
  undo_btn.pack(side=LEFT, padx=2, pady=2)
  createToolTip(undo_btn, "Undo")

  # Redo Button
  global redo_btn
  redo_btn = Button(toolbar, image=undo_icon, command=redo_text, relief=FLAT)
  redo_btn.image = undo_icon
  redo_btn.pack(side=LEFT, padx=2, pady=2)
  createToolTip(redo_btn, "Redo")

  # Exit Button
  global close_btn
  close_btn = Button(toolbar, image=close_icon, command=close_window, relief=FLAT)
  close_btn.image = close_icon
  close_btn.pack(side="right", padx=5, pady=2)
  createToolTip(close_btn, "Exit")

  # Minimize Button
  global min_btn
  min_btn = Button(toolbar, image=minimize_icon, command=minimize_window, relief=FLAT)
  min_btn.image = minimize_icon
  min_btn.pack(side="right", padx=2, pady=2)
  createToolTip(min_btn, "Minimize")


  # Maximize Button
  # global max_btn
  # max_btn = Button(toolbar, image=maximize_icon, command=maximize_window, relief=FLAT)
  # max_btn.image = maximize_icon
  # max_btn.pack(side="right",padx=2, pady=2)
  # createToolTip(max_btn, "Maximize")

  # Toogle Button for theme
  toggle_theme_btn = Button(toolbar, text="Theme", command=toggle_theme, relief=FLAT)
  toggle_theme_btn.pack(side=RIGHT, pady=2)
  createToolTip(toggle_theme_btn, "Light Mode / Dark Mode")

  toolbar.pack(side=TOP, fill=X)


  
  
  #Mic Button
  global mic_btn
  mic_btn = Button(toolbar, image=mic_icon, command=activate_commands, relief=FLAT)
  mic_btn.image = mic_icon
  mic_btn.pack (side="right", padx=2, pady=2)
  createToolTip(mic_btn, "Listen")

############################################################################################
######                                                               ######
############################################################################################

create_toolbar_top()

# Voice command feedback area
voice_command_feedback = Text(Honey_screen, height=3, font = Font(family="Courier New", size=20, weight="bold"), state=DISABLED, bg=light_theme["output_bg"], fg=light_theme["output_fg"])
voice_command_feedback.pack(side=BOTTOM, fill=X)
voice_command_feedback.config()

screen_height = Honey_screen.winfo_screenheight()

global editor
editor = Text(Honey_screen, undo=True, relief=FLAT)
editor.pack(side=LEFT, fill=BOTH, expand=False, padx=10, pady=20)
editor.bind('<Key>', check_text_and_toggle_buttons)

disabled_buttons(DISABLED)
enable_buttons(DISABLED)

start_listening()

Honey_screen.attributes('-fullscreen', True)
# Honey_screen.config(bg='#FFCF81')

# Honey_screen.overrideredirect(True)  # This removes the window decorations
Honey_screen.mainloop()
