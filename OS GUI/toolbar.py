import tkinter as tk
from tkinter import LEFT, RIGHT, FLAT, X

class Toolbar(tk.Frame):
    def __init__(self, master, icons, callbacks, create_tooltip, **kwargs):
        super().__init__(master, relief=FLAT, **kwargs)
        self.commands = callbacks
        self.icons = icons
        self.callbacks = callbacks
        self.create_tooltip = create_tooltip
class ToolbarTop(Toolbar):
    def __init__(self, master, icons, callbacks, create_tooltip, **kwargs):
        super().__init__(master, icons, callbacks, create_tooltip, **kwargs)
        
        self.mic_btn = tk.Button(self, image=self.icons["mic"], command=self.callbacks["activate_commands"], relief=FLAT)
        self.mic_btn.image = self.icons["mic"]
        self.mic_btn.pack(side=RIGHT, padx=2, pady=2)
        self.create_tooltip(self.mic_btn, "Listen")

        # Toggle Theme Button
        toggle_theme_btn = tk.Button(self, text="Theme", command=self.callbacks["toggle_theme"], relief=FLAT)
        toggle_theme_btn.pack(side=RIGHT, pady=2)
        self.create_tooltip(toggle_theme_btn, "Light Mode / Dark Mode")



class ToolbarEditor(Toolbar):
    def __init__(self, master, icons, callbacks, create_tooltip, **kwargs):
        super().__init__(master, icons, callbacks, create_tooltip, **kwargs)

        # New File Button
        new_file_btn = tk.Button(self, image=self.icons["new_file"], command=self.callbacks["open_new_file"], relief=FLAT)
        new_file_btn.image = self.icons["new_file"]
        new_file_btn.pack(side=LEFT, padx=2, pady=2)
        self.create_tooltip(new_file_btn, "New File")

        # Open Existing File Button
        open_file_btn = tk.Button(self, image=self.icons["open_file"], command=self.callbacks["open_existing_file"], relief=FLAT)
        open_file_btn.image = self.icons["open_file"]
        open_file_btn.pack(side=LEFT, padx=2, pady=2)
        self.create_tooltip(open_file_btn, "Existing File")

        # Save Button
        self.save_btn = tk.Button(self, image=self.icons["save"], command=self.callbacks["save"], relief=FLAT)
        self.save_btn.image = self.icons["save"]
        self.save_btn.pack(side=LEFT, padx=2, pady=2)
        self.create_tooltip(self.save_btn, "Save")

        # Save As Button
        self.save_as_btn = tk.Button(self, image=self.icons["save_as"], command=self.callbacks["save_as"], relief=FLAT)
        self.save_as_btn.image = self.icons["save_as"]
        self.save_as_btn.pack(side=LEFT, padx=2, pady=2)
        self.create_tooltip(self.save_as_btn, "Save As")

        # Copy Button
        self.copy_btn = tk.Button(self, image=self.icons["copy"], command=self.callbacks["copy"], relief=FLAT)
        self.copy_btn.image = self.icons["copy"]
        self.copy_btn.pack(side=LEFT, padx=2, pady=2)
        self.create_tooltip(self.copy_btn, "Copy")

        # Paste Button
        self.paste_btn = tk.Button(self, image=self.icons["paste"], command=self.callbacks["paste"], relief=FLAT)
        self.paste_btn.image = self.icons["paste"]
        self.paste_btn.pack(side=LEFT, padx=2, pady=2)
        self.create_tooltip(self.paste_btn, "Paste")

        # Cut Button
        self.cut_btn = tk.Button(self, image=self.icons["cut"], command=self.callbacks["cut"], relief=FLAT)
        self.cut_btn.image = self.icons["cut"]
        self.cut_btn.pack(side=LEFT, padx=2, pady=2)
        self.create_tooltip(self.cut_btn, "Cut")

        # Undo Button
        self.undo_btn = tk.Button(self, image=self.icons["undo"], command=self.callbacks["undo"], relief=FLAT)
        self.undo_btn.image = self.icons["undo"]
        self.undo_btn.pack(side=LEFT, padx=2, pady=2)
        self.create_tooltip(self.undo_btn, "Undo")

        # Redo Button
        self.redo_btn = tk.Button(self, image=self.icons["redo"], command=self.callbacks["redo"], relief=FLAT)
        self.redo_btn.image = self.icons["redo"]
        self.redo_btn.pack(side=LEFT, padx=2, pady=2)
        self.create_tooltip(self.redo_btn, "Redo")
    