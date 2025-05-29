import cv2
import tkinter as tk
import time


class StartUp:
    def __init__(self, path, window_size=(800, 600), duration=14, fullscreen=False):
        self.path = path
        self.window_size = window_size
        self.duration = duration
        self.window_name = 'Video'
        self.cap = None
        self.fullscreen = fullscreen

    def _get_screen_size(self):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
        return width, height

    def _center_window(self):
        screen_width, screen_height = self._get_screen_size()
        x = (screen_width - self.window_size[0]) // 2
        y = (screen_height - self.window_size[1]) // 2 - 10
        cv2.moveWindow(self.window_name, x, y)

    def play(self):
        self.cap = cv2.VideoCapture(self.path)
        if not self.cap.isOpened():
            print("Error: Could not open video.")
            return

        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.resizeWindow(self.window_name, *self.window_size)
        self._center_window()

        start_time = time.time()

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Reached end of video or error occurred. Exiting.")
                break

            frame = cv2.resize(frame, self.window_size, interpolation=cv2.INTER_AREA)
            cv2.imshow(self.window_name, frame)

            # Exit after duration or user interruption
            if time.time() - start_time > self.duration:
                break

            if cv2.waitKey(15) & 0xFF == ord('q') or cv2.getWindowProperty(
                    self.window_name, cv2.WND_PROP_VISIBLE) < 1:
                break

        self.cap.release()
        cv2.destroyAllWindows()