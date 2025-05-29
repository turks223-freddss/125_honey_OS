# bluefire_ide/ui_elements.py

from tkinter import Text, Button, Frame, LEFT, FLAT
from tooltips import ToolTip, createToolTip
from icons import iconsD
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

def create_editor_toolbar(parent):
    toolbar = Frame(parent, relief=FLAT)
    toolbar.pack(fill='x')

    buttons = {}

   # New File Button
    buttons['new_file_btn'] = Button(toolbar, image=iconsD['new_file'], command=open_new_file, relief=FLAT)
    buttons['new_file_btn'].pack(side=LEFT, padx=2, pady=2)
    createToolTip(buttons['new_file_btn'], "New File")

    # Open File Button
    buttons['open_file_btn'] = Button(toolbar, image=iconsD['open_file'], command=open_file, relief=FLAT)
    buttons['open_file_btn'].pack(side=LEFT, padx=2, pady=2)
    createToolTip(buttons['open_file_btn'], "Existing File")

    # Save Button
    buttons['save_btn'] = Button(toolbar, image=iconsD['save'], command=save, relief=FLAT)
    buttons['save_btn'].pack(side=LEFT, padx=2, pady=2)
    createToolTip(buttons['save_btn'], "Save")

    # Save As Button
    buttons['save_as_btn'] = Button(toolbar, image=iconsD['save_as'], command=save_as, relief=FLAT)
    buttons['save_as_btn'].pack(side=LEFT, padx=2, pady=2)
    createToolTip(buttons['save_as_btn'], "Save As")

    # Copy Button
    buttons['copy_btn'] = Button(toolbar, image=iconsD['copy'], command=copy, relief=FLAT)
    buttons['copy_btn'].image = iconsD['copy']
    buttons['copy_btn'].pack(side=LEFT, padx=2, pady=2)
    createToolTip(buttons['copy_btn'], "Copy")

    # Paste Button
    buttons['paste_btn'] = Button(toolbar, image=iconsD['paste'], command=paste, relief=FLAT)
    buttons['paste_btn'].image = iconsD['paste']
    buttons['paste_btn'].pack(side=LEFT, padx=2, pady=2)
    createToolTip(buttons['paste_btn'], "Paste")

    # Cut Button
    buttons['cut_btn'] = Button(toolbar, image=iconsD['cut'], command=cut, relief=FLAT)
    buttons['cut_btn'].image = iconsD['cut']
    buttons['cut_btn'].pack(side=LEFT, padx=2, pady=2)
    createToolTip(buttons['cut_btn'], "Cut")

    # Undo Button
    buttons['undo_btn'] = Button(toolbar, image=iconsD['undo'], command=undo, relief=FLAT)
    buttons['undo_btn'].image = iconsD['undo']
    buttons['undo_btn'].pack(side=LEFT, padx=2, pady=2)
    createToolTip(buttons['undo_btn'], "Undo")

    # Redo Button
    buttons['redo_btn'] = Button(toolbar, image=iconsD['redo'], command=redo, relief=FLAT)
    buttons['redo_btn'].image = iconsD['redo']
    buttons['redo_btn'].pack(side=LEFT, padx=2, pady=2)
    createToolTip(buttons['redo_btn'], "Redo")

    return toolbar, buttons
    # # Close Button
    # close_btn = Button(toolbar, image=iconsD['close'], command=close_window, relief=FLAT)
    # close_btn.image = iconsD['close']
    # close_btn.pack(side="right", padx=5, pady=2)
    # createToolTip(close_btn, "Exit")

    # # Minimize Button
    # min_btn = Button(toolbar, image=iconsD['minimize'], command=minimize_window, relief=FLAT)
    # min_btn.image = iconsD['minimize']
    # min_btn.pack(side="right", padx=2, pady=2)
    # createToolTip(min_btn, "Minimize")