import tkinter as tk
from PIL import Image, ImageTk

class DesktopIcon(tk.Frame):
    def __init__(self, master, text, image_path, open_callback, grid_size=100):
        super().__init__(master, width=grid_size, height=grid_size, bg="#fadba2")
        self.grid_size = grid_size
        self.open_callback = open_callback

        # Load and resize the icon image
        img = Image.open(image_path)
        img = img.resize((grid_size - 20, grid_size - 40), Image.Resampling.LANCZOS)  # leave some padding
        self.icon_image = ImageTk.PhotoImage(img)

        # Create label for image and text
        self.icon_label = tk.Label(self, image=self.icon_image, bg="#fadba2")
        self.icon_label.pack(side="top", pady=(5, 0))

        self.text_label = tk.Label(self, text=text, bg="#fadba2", fg="black", wraplength=grid_size-10)
        self.text_label.pack(side="top", pady=(2, 5))

        # Bind drag and double-click events on both labels
        for widget in (self, self.icon_label, self.text_label):
            widget.bind("<ButtonPress-1>", self.start_drag)
            widget.bind("<B1-Motion>", self.do_drag)
            widget.bind("<ButtonRelease-1>", self.stop_drag)
            widget.bind("<Double-Button-1>", lambda e: self.open_callback())

        self._drag_data = {"x": 0, "y": 0}

    def start_drag(self, event):
        self._drag_data = {
            "x": event.x,
            "y": event.y,
            "start_col": self.winfo_x() // self.grid_size,
            "start_row": self.winfo_y() // self.grid_size,
        }

    def do_drag(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        new_x = self.winfo_x() + dx
        new_y = self.winfo_y() + dy
        self.place(x=new_x, y=new_y)

    def stop_drag(self, event):
        parent = self.master
        snapped_col = max(0, min((self.winfo_x() + self.grid_size // 2) // self.grid_size,
                                parent.width // self.grid_size - 1))
        snapped_row = max(0, min((self.winfo_y() + self.grid_size // 2) // self.grid_size,
                                parent.height // self.grid_size - 1))
        snapped_cell = (snapped_col, snapped_row)

        # Check if spot taken
        for icon in parent.icons:
            if icon is not self:
                ix = icon.winfo_x() // self.grid_size
                iy = icon.winfo_y() // self.grid_size
                if (ix, iy) == snapped_cell:
                    old_col = self._drag_data.get("start_col", 0)
                    old_row = self._drag_data.get("start_row", 0)
                    self.place(x=old_col * self.grid_size, y=old_row * self.grid_size)
                    return

        x = snapped_col * self.grid_size
        y = snapped_row * self.grid_size
        self.place(x=x, y=y)

        old_col = self._drag_data.get("start_col", 0)
        old_row = self._drag_data.get("start_row", 0)
        parent.occupied_cells.discard((old_col, old_row))
        parent.occupied_cells.add((snapped_col, snapped_row))
