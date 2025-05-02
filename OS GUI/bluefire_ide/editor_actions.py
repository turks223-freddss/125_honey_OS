def cut(editor):
    editor.event_generate("<<Cut>>")

def copy(editor):
    editor.event_generate("<<Copy>>")

def paste(editor):
    editor.event_generate("<<Paste>>")

def undo(editor):
    editor.edit_undo()

def redo(editor):
    editor.edit_redo()
