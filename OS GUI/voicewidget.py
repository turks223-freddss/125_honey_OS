import tkinter as tk
from tkinter.font import Font

class VoiceAssistantWidget(tk.Frame):
    def __init__(self, parent, x=100, y=500, width=600, height=80, bg="#2a2a2a", fg="white", font_size=20):
        super().__init__(parent, bg=bg)

        self.parent = parent  # Needed for size info
        self.width = width
        self.height = height

        self.text_display = tk.Text(
            self,
            height=3,
            font=Font(family="Courier New", size=font_size, weight="bold"),
            state=tk.DISABLED,
            bg=bg,
            fg=fg,
            bd=0,
            relief="flat"
        )
        self.text_display.pack(fill=tk.BOTH, expand=True)

        self.place(x=x, y=y, width=width, height=height)

        self._offset_x = 0
        self._offset_y = 0
        self._bind_dragging()

    def _bind_dragging(self):
        self.text_display.bind("<Button-1>", self._start_drag)
        self.text_display.bind("<B1-Motion>", self._do_drag)
        self.bind("<Button-1>", self._start_drag)
        self.bind("<B1-Motion>", self._do_drag)

    def _start_drag(self, event):
        self._offset_x = event.x
        self._offset_y = event.y

    def _do_drag(self, event):
        # Calculate new position
        new_x = self.winfo_x() + event.x - self._offset_x
        new_y = self.winfo_y() + event.y - self._offset_y

        # Get parent window dimensions
        self.parent.update_idletasks()
        max_x = self.parent.winfo_width() - self.width
        max_y = self.parent.winfo_height() - self.height

        # Clamp the new position within boundaries
        new_x = max(0, min(new_x, max_x))
        new_y = max(0, min(new_y, max_y))

        self.place(x=new_x, y=new_y)

    def show_feedback(self, message: str):
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert(tk.END, message)
        self.text_display.config(state=tk.DISABLED)
