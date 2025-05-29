import threading
import speech_recognition as sr
from tkinter import NORMAL, END

class VoiceAssistant:
    def __init__(self, mic_btn, feedback_widget, icons, callbacks, is_dark_mode_fn, calculator_state_fn, calculator_obj):
        self.recognizer = sr.Recognizer()
        self.mic_btn = mic_btn
        self.feedback = feedback_widget
        self.icons = icons
        self.callbacks = callbacks
        self.is_dark_mode = is_dark_mode_fn
        self.is_calculator_active = calculator_state_fn
        self.calculator = calculator_obj

    def display_feedback(self, text):
        self.feedback.config(state=NORMAL)
        self.feedback.delete('1.0', END)
        self.feedback.insert('1.0', text)
        self.feedback.config(state='disabled')

    def restore_mic_icon(self):
        self.mic_btn.config(image=self.icons["mic"])
        self.mic_btn.image = self.icons["mic"]

    def start_listening(self):
        threading.Thread(target=self._listen_for_activation, daemon=True).start()

    def _listen_for_activation(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Say 'Honey' to activate commands...")
            while True:
                try:
                    audio_data = self.recognizer.listen(source)
                    text = self.recognizer.recognize_google(audio_data).lower()
                    if "honey" in text:
                        self.mic_btn.config(image=self.icons["mic_listen"])
                        self.mic_btn.image = self.icons["mic_listen"]
                        self.display_feedback("Yes, dear?")
                        threading.Thread(target=self._listen_and_process, daemon=True).start()
                        return
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(f"Mic error: {e}")

    def _listen_and_process(self):
        with sr.Microphone() as source:
            try:
                audio_data = self.recognizer.listen(source, timeout=5)
                command = self.recognizer.recognize_google(audio_data).lower()
                self.display_feedback(f"Okay, dear. Let me quickly do that for you... ({command})")

                if self.is_calculator_active() and "calculator" not in command:
                    self.calculator.set_input_from_string(command)
                    return

                command_map = {
                    ("new file please",): self.callbacks["new_file"],
                    ("existing file please", "abrihi"): self.callbacks["open_file"],
                    ("save please",): self.callbacks["save"],
                    ("save as please", "save us please"): self.callbacks["save_as"],
                    ("copy please",): self.callbacks["copy"],
                    ("cut please",): self.callbacks["cut"],
                    ("paste please",): self.callbacks["paste"],
                    ("undo please",): self.callbacks["undo"],
                    ("redo please",): self.callbacks["redo"],
                    ("minimize please",): self.callbacks["minimize"],
                    ("exit please", "shut up", "avada kedavra", "yamete"): self.callbacks["close"],
                    ("editor",): self.callbacks["editor"],
                    ("calculator",): self.callbacks["calculator"],
                }

                for phrases, action in command_map.items():
                    if any(p in command for p in phrases):
                        action()
                        return

                if "dark" in command and not self.is_dark_mode():
                    self.callbacks["toggle_theme"]()
                elif any(kw in command for kw in ["light mode please", "open the curtains"]) and self.is_dark_mode():
                    self.callbacks["toggle_theme"]()

            except Exception as e:
                self.display_feedback(f"Sorry, dear. I didn't quite get that... ({str(e)})")
            finally:
                self.restore_mic_icon()
