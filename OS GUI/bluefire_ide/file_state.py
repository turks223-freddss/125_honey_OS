# bluefire_ide/file_state.py

# Holds the file path state across modules

_file_path = ''

def set_file_path(path):
    global _file_path
    _file_path = path

def get_file_path():
    return _file_path
