    # bluefire_ide/file_operations.py

from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.messagebox
from tkinter import END
import os
from file_state import set_file_path, get_file_path


def open_new_file(editor, window, disabled_buttons_fn, display_feedback_fn):
    editor.delete('1.0', END)
    set_file_path('')  # Clear file path in shared state
    window.title('Bluefire - New File')
    display_feedback_fn('New file created.')
    disabled_buttons_fn('disabled')

def open_existing_file(editor, window, disabled_buttons_fn):
    from tkinter.filedialog import askopenfilename
    path = askopenfilename()

    if path:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            editor.delete('1.0', END)
            editor.insert('1.0', content)
            set_file_path(path)
            window.title(f'Bluefire - {os.path.basename(path)}')
            disabled_buttons_fn('disabled')

# Opens a .txt file and inserts it into the editor
def open_file(editor):
    path = askopenfilename(filetypes=[("Blue Files", "*.txt")])
    if not path:
        return
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', 'end')
        editor.insert('1.0', code)
        set_file_path(path)

# Saves content from the editor to file
def save(editor):
    code = editor.get('1.0', 'end').strip()
    if not code:
        tkinter.messagebox.showerror("Unable to Save", "There is no content to save.")
        return

    path = get_file_path()
    if not path:
        path = asksaveasfilename(defaultextension=".txt", filetypes=[("Blue Files", "*.txt")])
        if not path:
            return
        if not path.endswith(".txt"):
            path += ".txt"
        set_file_path(path)

    with open(path, 'w') as file:
        file.write(code)

# Always asks user to save as a new file
def save_as(editor):
    code = editor.get('1.0', 'end').strip()
    if not code:
        tkinter.messagebox.showerror("Unable to Save", "There is no content to save.")
        return

    path = asksaveasfilename(defaultextension=".txt", filetypes=[("Blue Files", "*.txt")])
    if not path:
        return
    if not path.endswith(".txt"):
        path += ".txt"

    with open(path, 'w') as file:
        file.write(code)
        set_file_path(path)
