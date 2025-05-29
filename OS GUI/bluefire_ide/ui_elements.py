# bluefire_ide/ui_elements.py

from tkinter import Text, Button, Frame, LEFT, FLAT
from tooltip import ToolTip, create_tooltip
from iconpaths import icon
from bluefire_ide import file_operations, editor_actions
from bluefire_ide.file_operations import save, save_as, open_file, open_existing_file, open_new_file
from bluefire_ide.editor_actions import copy, cut, paste, undo, redo



# Creates the text editor for writing code
def create_editor(parent):
    editor = Text(parent)
    editor.pack(fill='both', expand=True)
    return editor

# Creates a smaller text box for output/errors
def create_output_area(parent):
    output = Text(parent, height=8, bg='black', fg='white')
    output.pack(fill='x')
    return output
