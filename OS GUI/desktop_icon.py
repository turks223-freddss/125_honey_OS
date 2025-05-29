import tkinter as tk
from PIL import Image, ImageTk

class DesktopIcon(tk.Frame):
    selected_icon = None

    def __init__(self, master, text, image_path, open_callback, grid_size=100):
        super().__init__(master, width=grid_size, height=grid_size, highlightthickness=2)
        self.grid_size = grid_size
        self.open_callback = open_callback
        self.default_bg = "#fadba2"
        self.selected_bg = "#bcd9ff"

        self.configure(bg=self.default_bg, highlightbackground=self.default_bg)

        img = Image.open(image_path)
        img = img.resize((grid_size - 20, grid_size - 40), Image.Resampling.LANCZOS)
        self.icon_image = ImageTk.PhotoImage(img)

        self.icon_label = tk.Label(self, image=self.icon_image, bg=self.default_bg)
        self.icon_label.pack(side="top", pady=(5, 0))

        self.text_label = tk.Label(self, text=text, bg=self.default_bg, fg="black", wraplength=grid_size - 10)
        self.text_label.pack(side="top", pady=(2, 5))

        for widget in (self, self.icon_label, self.text_label):
            widget.bind("<ButtonPress-1>", self.on_button_press)
            widget.bind("<B1-Motion>", self.do_drag)
            widget.bind("<ButtonRelease-1>", self.on_button_release)
            widget.bind("<Double-Button-1>", self.on_double_click)

        self._drag_data = {"x": 0, "y": 0, "dragging": False}

    def on_button_press(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        self._drag_data["dragging"] = False
        # Save original pos for snapping later
        self._drag_data["start_col"] = self.winfo_x() // self.grid_size
        self._drag_data["start_row"] = self.winfo_y() // self.grid_size

    def do_drag(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        distance = abs(dx) + abs(dy)

        # If user moved mouse enough, consider it dragging
        if distance > 3:
            self._drag_data["dragging"] = True

        if self._drag_data["dragging"]:
            new_x = self.winfo_x() + dx
            new_y = self.winfo_y() + dy
            self.place(x=new_x, y=new_y)

    def on_button_release(self, event):
        if self._drag_data["dragging"]:
            # Drag finished, snap to grid
            parent = self.master
            snapped_col = max(0, min((self.winfo_x() + self.grid_size // 2) // self.grid_size,
                                     parent.width // self.grid_size - 1))
            snapped_row = max(0, min((self.winfo_y() + self.grid_size // 2) // self.grid_size,
                                     parent.height // self.grid_size - 1))
            snapped_cell = (snapped_col, snapped_row)

            for icon in parent.icons:
                if icon is not self:
                    ix = icon.winfo_x() // self.grid_size
                    iy = icon.winfo_y() // self.grid_size
                    if (ix, iy) == snapped_cell:
                        old_col = self._drag_data["start_col"]
                        old_row = self._drag_data["start_row"]
                        self.place(x=old_col * self.grid_size, y=old_row * self.grid_size)
                        return

            x = snapped_col * self.grid_size
            y = snapped_row * self.grid_size
            self.place(x=x, y=y)

            old_col = self._drag_data["start_col"]
            old_row = self._drag_data["start_row"]
            parent.occupied_cells.discard((old_col, old_row))
            parent.occupied_cells.add((snapped_col, snapped_row))
        else:
            # No dragging → treat as a click: select icon
            self.select_icon()

    def select_icon(self):
        if DesktopIcon.selected_icon and DesktopIcon.selected_icon is not self:
            DesktopIcon.selected_icon.deselect()

        self.select()
        DesktopIcon.selected_icon = self

    def select(self):
        self.config(highlightbackground="blue")
        self.icon_label.config(bg=self.selected_bg)
        self.text_label.config(bg=self.selected_bg)

    def deselect(self):
        self.config(highlightbackground=self.default_bg)
        self.icon_label.config(bg=self.default_bg)
        self.text_label.config(bg=self.default_bg)

    def on_double_click(self, event):
        self.open_callback()
