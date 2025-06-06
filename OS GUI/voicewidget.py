import tkinter as tk
from tkinter.font import Font
from PIL import Image, ImageTk


class VoiceAssistantWidget(tk.Frame):
    def __init__(self, parent, x=100, y=500, width=600, height=80,
        bg="#2a2a2a", fg="white", font_size=20, button_command=None, mic_icon=None):
        super().__init__(parent, bg=bg)
        self.mic_icon = mic_icon
        self.parent = parent
        self.width = width
        self.height = height

        mic_img = Image.open("OS GUI/assets/microphone.png")
        mic_img = mic_img.resize((40, 40), Image.LANCZOS)
        mic_icon = ImageTk.PhotoImage(mic_img)

        # Use grid layout for precise control
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)  # Button column
        self.rowconfigure(0, weight=1)

        # Text display
        self.text_display = tk.Text(
            self,
            font=Font(family="Courier New", size=font_size, weight="bold"),
            state=tk.DISABLED,
            bg=bg,
            fg=fg,
            bd=0,
            relief="flat",
            wrap="word"
        )
        self.text_display.tag_configure("margin", lmargin1=10, lmargin2=10, rmargin=10)
        self.text_display.grid(row=0, column=0, sticky="nsew", padx=(10, 10))
        
        self.button_command = button_command

        self.action_button = tk.Button(
            self,
            image=self.mic_icon,  # Or "✕" or any icon/text you like
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#444444",
            bd=0,
            relief="flat",
            command=self.button_command,  # <- bound to external function
            cursor="hand2",
            width=40
        )
        self.action_button.grid(row=0, column=1, sticky="ns")

        self.place(x=x, y=y, width=width, height=height)

        self._offset_x = 0
        self._offset_y = 0
        self._bind_dragging()

    def _bind_dragging(self):
        for widget in (self.text_display, self.action_button, self):
            widget.bind("<Button-1>", self._start_drag)
            widget.bind("<B1-Motion>", self._do_drag)

    def _start_drag(self, event):
        self._offset_x = event.x
        self._offset_y = event.y

    def _do_drag(self, event):
        new_x = self.winfo_x() + event.x - self._offset_x
        new_y = self.winfo_y() + event.y - self._offset_y

        self.parent.update_idletasks()
        max_x = self.parent.winfo_width() - self.width
        max_y = self.parent.winfo_height() - self.height

        new_x = max(0, min(new_x, max_x))
        new_y = max(0, min(new_y, max_y))

        self.place(x=new_x, y=new_y)

    def show_feedback(self, message: str):
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert(tk.END, "\n" + message, "margin")
        self.text_display.config(state=tk.DISABLED)

    def on_button_click(self):
        # This will just show a test message
        self.show_feedback("Button clicked!")
