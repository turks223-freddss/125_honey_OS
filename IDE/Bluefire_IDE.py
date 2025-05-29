from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import tkinter.messagebox
from tkinter import Tk
import subprocess

compiler = Tk()
compiler.title('Bluefire IDE')
file_path = ''



def set_file_path(path):
    global file_path
    file_path = path

def open_file():
    path = askopenfilename(filetypes=[('Blue Files', '*.blu')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)

def save():
    global file_path
    # Check if the editor has content to save
    code = editor.get('1.0', END).strip()
    if not code:
        # You can provide a message to the user or handle the empty content scenario here
        tkinter.messagebox.showerror("Unable to Save", "There is no content to save.")
        return
    
    elif file_path == '':
        path = asksaveasfilename(filetypes=[('Blue Files', '*.blu')])
        if not path:  # Check if the user canceled the save dialog
            return  # Do nothing if the user canceled
            
        if not path.endswith('.blu'):  # Add .blu extension if not already present
            path += '.blu'
        file_path = path

    
    with open(path, 'w') as file:
        file.write(code)
        set_file_path(path)



def save_as():
    code = editor.get('1.0', END).strip()
    if not code:
        tkinter.messagebox.showerror("Unable to Save", "There is no content to save.")
        return

    path = asksaveasfilename(filetypes=[('Blue Files', '*.blu')])
    if not path:
        return

    if not path.endswith('.blu'):
        path += '.blu'

    with open(path, 'w') as file:
        file.write(code)
        set_file_path(path)


def run():
    if file_path == '':
        save_prompt = Toplevel()
        text = Label(save_prompt, text = 'Huy! Please save code first!')
        text.pack()
        return
    
    command = f'python {file_path}'
    process = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    output, error =  process. communicate()
    code_output.insert('1.0', output)
    code_output.insert('1.0', error)
    
menu_bar = Menu(compiler)

file_menu =  Menu(menu_bar, tearoff=0)
file_menu.add_command(label = 'New File', command=run)
menu_bar.add_cascade(label = 'New File', menu = file_menu)

OpenFile_menu = Menu(menu_bar, tearoff = 0)
OpenFile_menu.add_command(label = 'Open File', command= open_file)
OpenFile_menu.add_cascade(label = 'Open File', menu = OpenFile_menu)

save_bar =  Menu(menu_bar, tearoff=0)
save_bar.add_command(label = 'Save', command=save)
menu_bar.add_cascade(label = 'Save', menu = save_bar)

save_as_bar =  Menu(menu_bar, tearoff=0)
save_as_bar.add_command(label = 'Save As', command=save_as)
menu_bar.add_cascade(label = 'Save As', menu = save_as_bar)

run_bar =  Menu(menu_bar, tearoff=0)
run_bar.add_command(label = 'Run', command=run)
menu_bar.add_cascade(label = 'Run', menu = run_bar)

compile_bar =  Menu(menu_bar, tearoff=0)
compile_bar.add_command(label = 'Compile', command=compile)
menu_bar.add_cascade(label = 'Compile', menu = compile_bar)

compiler.config(menu = menu_bar)

editor = Text()
editor.pack()

code_output = Text(height = 8)
code_output.pack() 

compiler.mainloop()
