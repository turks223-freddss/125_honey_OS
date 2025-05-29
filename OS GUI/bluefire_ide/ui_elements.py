# bluefire_ide/ui_elements.py

from tkinter import Text

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
