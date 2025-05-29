import tkinter as tk
from tkinter import ttk
from datetime import datetime

class Taskbar(tk.Frame):
    def __init__(self, master=None, apps=None, app_callbacks=None, **kwargs):
        super().__init__(master, bg="#1e1e1e", height=40, **kwargs)

        self.launchers = apps or []
        self.callbacks = app_callbacks or {}
        self.opened = {}  # app_name -> {"widget": app_window, "button": task_button}

        self._build_ui()

        self.start_menu = None
        self.start_menu_visible = False

    def _build_ui(self):
        # Left side frame for launchers + tasks
        left_frame = tk.Frame(self, bg="#1e1e1e")
        left_frame.pack(side="left", fill="y")

        # Start Button
        self.start_button = ttk.Button(left_frame, text="Start", width=6,
        command=self.toggle_start_menu)
        self.start_button.pack(side="left", padx=5, pady=6)

        # Launcher Buttons
        for app in self.launchers:
            btn = ttk.Button(left_frame, text=app,
                             command=lambda a=app: self.launch_custom_app(a))
            btn.pack(side="left", padx=4, pady=6)

        # Frame to hold opened app task buttons
        self.tasks_frame = tk.Frame(left_frame, bg="#1e1e1e")
        self.tasks_frame.pack(side="left", padx=8, pady=6)

        # Spacer in middle
        spacer = tk.Label(self, bg="#1e1e1e")
        spacer.pack(side="left", expand=True)

        # Right side frame for system indicators + clock
        right_frame = tk.Frame(self, bg="#1e1e1e")
        right_frame.pack(side="right", fill="y", padx=10)

        # Battery icon (fake static)
        self.battery_label = tk.Label(right_frame, text="🔋 85%", fg="white",
                                      bg="#1e1e1e", font=("Segoe UI", 10))
        self.battery_label.pack(side="left", padx=5)

        # WiFi icon (fake static)
        self.wifi_label = tk.Label(right_frame, text="📶", fg="white",
                                   bg="#1e1e1e", font=("Segoe UI", 10))
        self.wifi_label.pack(side="left", padx=5)

        # Clock label (rightmost)
        self.clock_label = tk.Label(right_frame, fg="white", bg="#1e1e1e",
                                    font=("Segoe UI", 10))
        self.clock_label.pack(side="left", padx=5)
        self._update_clock()

    def _update_clock(self):
        now = datetime.now().strftime('%H:%M:%S')
        self.clock_label.config(text=now)
        self.after(1000, self._update_clock)

    def launch_custom_app(self, app_name):
        # Call the app toggle callback if exists
        if app_name in self.callbacks:
            self.callbacks[app_name](self)  # pass self for tracking
        else:
            self.launch_app(app_name)  # fallback for dummy apps

    def launch_app(self, app_name):
        # Dummy generic launcher opens a Toplevel window
        if app_name in self.opened:
            self.toggle_task(app_name)
            return

        win = tk.Toplevel(self)
        win.title(app_name)
        win.geometry("400x300+200+200")
        lbl = tk.Label(win, text=f"This is {app_name}", font=("Segoe UI", 14))
        lbl.pack(expand=True)

        self.add_task(app_name, win)

        # When window closes, remove task button
        def on_close():
            self.remove_task(app_name)
            win.destroy()

        win.protocol("WM_DELETE_WINDOW", on_close)

    def add_task(self, app_name, widget):
        if app_name in self.opened:
            return  # already tracked

        # Create task button
        btn = ttk.Button(self.tasks_frame, text=app_name,
                         command=lambda n=app_name: self.toggle_task(n))
        btn.pack(side="left", padx=2, pady=6)

        self.opened[app_name] = {"widget": widget, "button": btn}

    def remove_task(self, app_name):
        if app_name not in self.opened:
            return
        entry = self.opened.pop(app_name)
        entry["button"].destroy()

    def toggle_task(self, app_name):
        if app_name not in self.opened:
            return
        win = self.opened[app_name]["widget"]

        # Toggle visibility/minimized state
        if win.state() == "normal":
            win.withdraw()  # minimize (hide)
        else:
            win.deiconify()  # restore
            win.lift()       # bring to front
    

    def toggle_start_menu(self):
        if self.start_menu_visible:
            self.hide_start_menu()
        else:
            self.show_start_menu()

    def show_start_menu(self):
        if self.start_menu is None or not self.start_menu.winfo_exists():
            self.start_menu = tk.Toplevel(self)
            self.start_menu.overrideredirect(True)
            self.start_menu.configure(bg="#2c2c2c", borderwidth=2, relief="raised")

            # Container frame with padding
            container = tk.Frame(self.start_menu, bg="#2c2c2c", padx=10, pady=10)
            container.pack(fill="both", expand=True)

            # Menu items: (label, callback)
            menu_items = [
                ("📁 Files", lambda: self._launch_app_from_menu("Files")),
                ("⏻ Shutdown ", lambda: self._launch_app_from_menu("Terminal")),
                ("⚙️ Settings", lambda: self._launch_app_from_menu("Settings")),
            ]

            # Create buttons with hover style
            for text, cmd in menu_items:
                btn = tk.Label(container, text=text, bg="#2c2c2c", fg="white",
                font=("Segoe UI", 12), anchor="w", padx=12, pady=8, cursor="hand2")
                btn.pack(fill="x", pady=3)

                btn.bind("<Button-1>", lambda e, c=cmd: c())
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#3a3a3a"))
                btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#2c2c2c"))

            # Close menu if clicking outside
            self.start_menu.bind("FocusOut", lambda e: self.hide_start_menu())

        # Position menu just above Start button
        btn_x = self.start_button.winfo_rootx()
        btn_y = self.start_button.winfo_rooty()
        btn_height = self.start_button.winfo_height()

        # Calculate menu height dynamically
        self.start_menu.update_idletasks()
        menu_width = 180
        menu_height = self.start_menu.winfo_height()

        x = btn_x
        y = btn_y - menu_height

        self.start_menu.geometry(f"{menu_width}x{menu_height}+{x}+{y}")
        self.start_menu.deiconify()
        self.start_menu.lift()
        self.start_menu.focus_set()
        self.start_menu_visible = True

    def hide_start_menu(self):
        if self.start_menu and self.start_menu.winfo_exists():
            self.start_menu.withdraw()
        self.start_menu_visible = False

    def _launch_app_from_menu(self, app_name):
        # Hide start menu first
        self.hide_start_menu()

        # Call app callback if exists
        if app_name in self.callbacks:
            self.callbacks[app_name](self)
        else:
            self.launch_app(app_name) 