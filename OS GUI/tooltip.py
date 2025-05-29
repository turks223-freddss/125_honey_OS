from tkinter import Toplevel, Label, LEFT, SOLID


class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.text = None

    def showtip(self, text):
        """Display text in tooltip window"""
        self.text = text
        if self.tipwindow or not self.text:
            return

        self.tipwindow = tw = Toplevel(self.widget)
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx()
        y += self.widget.winfo_rooty() + self.widget.winfo_height()

        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(
            tw,
            text=self.text,
            justify=LEFT,
            background="#ffffe0",
            relief=SOLID,
            borderwidth=1,
            font=("tahoma", "10", "normal")
        )
        label.pack(ipadx=1)

    def hidetip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


def create_tooltip(widget, text):
    """Attach a tooltip to any Tkinter widget."""
    tooltip = ToolTip(widget)

    def on_enter(event):
        tooltip.showtip(text)

    def on_leave(event):
        tooltip.hidetip()

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)
