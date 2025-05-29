# bluefire_ide/main.py

from tkinter import Tk, NORMAL, DISABLED
from .file_operations import open_file, save, save_as
from .runner import run
from .ui_elements import create_editor, create_output_area, create_editor_toolbar
from .editor_state import changes_monitor


def main():
    app = Tk()
    app.title("Bluefire IDE")

    editor = create_editor(app)
    output = create_output_area(app)

    toolbar, buttons = create_editor_toolbar(app, editor, output)
    changes_monitor(editor, save, save_as)
    app.mainloop()

if __name__ == '__main__':
    main()
