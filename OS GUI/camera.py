import cv2
import os
from datetime import datetime
from tkinter import Frame, Label, Button, StringVar, PhotoImage, LEFT, RIGHT, TOP
from PIL import Image, ImageTk, ImageDraw

class CameraViewer:
    def __init__(self, parent):
        self.parent = parent
        self.container = None
        self.video_capture = None
        self.running = False
        self.label = None
        self.imgtk = None
        self.current_frame = None
        self.status_var = StringVar()

        self.image_files = []
        self.current_image_index = -1
        self.thumbnail_label = None

        self.overlay = None
        self.overlay_image_label = None
        self.drag_data = {"x": 0, "y": 0}

    def create_camera_icon_image(self, size=48):
        img = Image.new("RGBA", (size, size), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        radius = size // 2

        draw.ellipse((0, 0, size-1, size-1), fill="#d32f2f")

        body_w, body_h = size * 0.6, size * 0.4
        body_x = (size - body_w) / 2
        body_y = (size - body_h) / 2 + 4
        draw.rectangle([body_x, body_y, body_x + body_w, body_y + body_h], fill="white")

        lens_radius = size * 0.1
        lens_center_x = size / 2
        lens_center_y = body_y + body_h / 2
        draw.ellipse([
            lens_center_x - lens_radius, lens_center_y - lens_radius,
            lens_center_x + lens_radius, lens_center_y + lens_radius], fill="#d32f2f")

        vf_w, vf_h = body_w * 0.4, body_h * 0.4
        vf_x = (size - vf_w) / 2
        vf_y = body_y - vf_h + 2
        draw.rectangle([vf_x, vf_y, vf_x + vf_w, vf_y + vf_h], fill="white")

        return ImageTk.PhotoImage(img)

    def create_camera_panel(self):
        if self.container is not None:
            self.container.place(x=50, y=50)
            return

        self.container = Frame(self.parent, bg="black", bd=2, relief="sunken")
        self.container.place(x=50, y=50)

        header = Frame(self.container, bg="gray20")
        header.pack(fill="x")
        header.bind("<ButtonPress-1>", self.start_move)
        header.bind("<B1-Motion>", self.do_move)

        title = Label(header, text="Camera App", fg="white", bg="gray20", font=("Arial", 10, "bold"))
        title.pack(side="left", padx=5)

        close_top_btn = Button(header, text="✖", command=self.close_camera,
                               bg="red", fg="white", font=("Arial", 10, "bold"), bd=0, cursor="hand2")
        close_top_btn.pack(side="right", padx=5, pady=2)

        self.label = Label(self.container, bg="black")
        self.label.pack(pady=(10, 5))

        controls_frame = Frame(self.container, bg="black")
        controls_frame.pack(fill="x", pady=(0, 10))

        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_rowconfigure(0, weight=1)

        self.camera_icon_img = self.create_camera_icon_image(48)

        self.snap_btn = Button(controls_frame, image=self.camera_icon_img,
                               command=self.take_picture,
                               bg="#000000", activebackground="#000000",
                               bd=0, relief="flat", cursor="hand2",
                               highlightthickness=0)
        self.snap_btn.image = self.camera_icon_img
        self.snap_btn.grid(row=0, column=0, pady=5, padx=(60,5))

        self.thumbnail_label = Label(controls_frame, bg="gray20", cursor="hand2", bd=2, relief="groove")
        self.thumbnail_label.grid(row=0, column=1, padx=10)
        self.thumbnail_label.bind("<Button-1>", self.show_image_overlay)

        status_label = Label(self.container, textvariable=self.status_var, fg="yellow", font=("Arial", 9), bg="black")
        status_label.pack(side="bottom", pady=(0, 5))

        self.load_images()
        self.display_current_thumbnail()

    def start_move(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def do_move(self, event):
        x = self.container.winfo_x() + event.x - self.drag_data["x"]
        y = self.container.winfo_y() + event.y - self.drag_data["y"]
        self.container.place(x=x, y=y)

    def open_camera(self):
        self.create_camera_panel()

        if self.running:
            return

        self.video_capture = cv2.VideoCapture(0)
        if not self.video_capture.isOpened():
            self.status_var.set("Error: Cannot open camera")
            return

        self.status_var.set("Camera opened. Ready to take pictures.")
        self.running = True
        self.update_frame()

    def update_frame(self):
        if not self.running:
            return

        ret, frame = self.video_capture.read()
        if ret:
            self.current_frame = frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            self.imgtk = ImageTk.PhotoImage(image=img)
            self.label.config(image=self.imgtk)

        self.container.after(15, self.update_frame)

    def take_picture(self):
        if self.current_frame is not None:
            save_folder = "captured_images"
            os.makedirs(save_folder, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{save_folder}/photo_{timestamp}.png"

            cv2.imwrite(filename, self.current_frame)
            self.status_var.set(f"Picture saved: {filename}")
            print(f"Saved picture: {filename}")
            self.image_files.append(filename)
            self.current_image_index = len(self.image_files) - 1
            self.display_current_thumbnail()
        else:
            self.status_var.set("No frame available to save!")

    def load_images(self):
        folder = "captured_images"
        if os.path.exists(folder):
            self.image_files = sorted(
                [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith('.png')],
                reverse=True
            )
            self.current_image_index = 0 if self.image_files else -1

    def display_current_thumbnail(self):
        if 0 <= self.current_image_index < len(self.image_files):
            try:
                img = Image.open(self.image_files[self.current_image_index])
                img.thumbnail((50, 50))
                img_tk = ImageTk.PhotoImage(img)
                self.thumbnail_label.config(image=img_tk)
                self.thumbnail_label.image = img_tk
            except Exception as e:
                print("Thumbnail error:", e)
        else:
            self.thumbnail_label.config(image="")
            self.thumbnail_label.image = None

    def show_image_overlay(self, event=None):
        if not self.image_files:
            return

        if self.overlay:
            self.overlay.destroy()

        self.overlay = Frame(self.container, bg="black", bd=2, relief="raised")
        self.overlay.place(relx=0.5, rely=0.5, anchor="center", width=320, height=320)

        overlay_header = Frame(self.overlay, bg="gray20")
        overlay_header.pack(fill="x")

        # Removed drag bindings:
        # overlay_header.bind("<ButtonPress-1>", self.start_overlay_move)
        # overlay_header.bind("<B1-Motion>", self.do_overlay_move)

        title = Label(overlay_header, text="Preview", fg="white", bg="gray20", font=("Arial", 9, "bold"))
        title.pack(side=LEFT, padx=5)

        close_btn = Button(overlay_header, text="✖", command=self.overlay.destroy,
                        bg="red", fg="white", font=("Arial", 9, "bold"), bd=0, cursor="hand2")
        close_btn.pack(side=RIGHT, padx=5)

        self.overlay_image_label = Label(self.overlay, bg="black")
        self.overlay_image_label.pack(expand=True)

        nav_frame = Frame(self.overlay, bg="black")
        nav_frame.pack(side="bottom", pady=5)

        left_btn = Button(nav_frame, text="◀", command=self.prev_image,
                        bg="gray", fg="white", width=4, cursor="hand2")
        left_btn.pack(side=LEFT, padx=5)

        right_btn = Button(nav_frame, text="▶", command=self.next_image,
                        bg="gray", fg="white", width=4, cursor="hand2")
        right_btn.pack(side=RIGHT, padx=5)

        self.display_overlay_image()
        self.overlay.bind_all("<Left>", lambda e: self.prev_image())
        self.overlay.bind_all("<Right>", lambda e: self.next_image())

    def close_image_overlay(self, event=None):
        if self.overlay:
            self.overlay.destroy()
            self.overlay = None

    def display_overlay_image(self):
        if self.overlay and 0 <= self.current_image_index < len(self.image_files):
            try:
                img = Image.open(self.image_files[self.current_image_index])
                img.thumbnail((280, 240))
                img_tk = ImageTk.PhotoImage(img)
                self.overlay_image_label.config(image=img_tk)
                self.overlay_image_label.image = img_tk
            except Exception as e:
                print("Overlay image error:", e)

    def prev_image(self):
        if self.image_files:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_files)
            self.display_overlay_image()

    def next_image(self):
        if self.image_files:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
            self.display_overlay_image()

    def close_camera(self):
        self.running = False
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None

        if self.container:
            self.container.place_forget()
        self.status_var.set("")
