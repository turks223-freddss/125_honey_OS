# bluefire_ide/main.py

from tkinter import Tk, Menu
from .file_operations import open_file, save, save_as
from .runner import run
from .ui_elements import create_editor, create_output_area

def main():
    app = Tk()
    app.title("Bluefire IDE")

    editor = create_editor(app)
    output = create_output_area(app)

    menu_bar = Menu(app)

    # File Menu
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label='Open File', command=lambda: open_file(editor))
    file_menu.add_command(label='Save', command=lambda: save(editor))
    file_menu.add_command(label='Save As', command=lambda: save_as(editor))
    menu_bar.add_cascade(label='File', menu=file_menu)

    # Run Menu
    run_menu = Menu(menu_bar, tearoff=0)
    run_menu.add_command(label='Run', command=lambda: run(output))
    menu_bar.add_cascade(label='Run', menu=run_menu)

    app.config(menu=menu_bar)
    app.mainloop()

if __name__ == '__main__':
    main()
