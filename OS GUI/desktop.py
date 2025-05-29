import tkinter as tk
from desktop_icon import DesktopIcon

class Desktop(tk.Frame):
    def __init__(self, master, grid_size=100):
        super().__init__(master, bg="#fadba2")
        self.grid_size = grid_size
        self.icons = []
        self.occupied_cells = set()

        self.bind("<Configure>", self._on_resize)
        self.width = 0
        self.height = 0

    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height

    def _grid_cell(self, x, y):
        """Convert pixel position to grid cell."""
        return (x // self.grid_size, y // self.grid_size)

    def _is_occupied(self, x, y):
        return (x, y) in self.occupied_cells

    def _mark_occupied(self, x, y):
        self.occupied_cells.add((x, y))

    def add_icon(self, text, image_path, open_callback, position=None):
        def place_when_ready():
            if self.width <= 1 or self.height <= 1:
                self.after(50, place_when_ready)
                return

            max_cols = self.width // self.grid_size
            max_rows = self.height // self.grid_size

            for row in range(max_rows):
                for col in range(max_cols):
                    if not self._is_occupied(col, row):
                        x = col * self.grid_size
                        y = row * self.grid_size

                        icon = DesktopIcon(self, text, image_path, open_callback, self.grid_size)
                        icon.place(x=x, y=y, width=self.grid_size, height=self.grid_size)

                        self.icons.append(icon)
                        self._mark_occupied(col, row)
                        return

            print("No space available for icon.")
        place_when_ready()
