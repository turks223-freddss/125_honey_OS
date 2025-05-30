import threading
import speech_recognition as sr
import app_callbacks as apps
from camera import CameraViewer

class VoiceController:
    def __init__(self, toolbar, icons, mic_icon, mic_listening_icon,
        display_feedback, calculator=None, editor=None,
        is_calculator_active=0, is_dark_mode=False):
        self.toolbar = toolbar
        self.icons = icons
        self.mic_icon = mic_icon
        self.mic_listening_icon = mic_listening_icon
        self.display_feedback = display_feedback
        self.calculator = calculator
        self.editor = editor
        self.is_calculator_active = is_calculator_active
        self.is_dark_mode = is_dark_mode
        self.listening = False

    def display_feedback_safe(self, message):
        # Schedule the UI update safely on the main thread
        self.toolbar.after(0, lambda: self.display_feedback(message))

    def stop_listening(self):
        self.listening = False

    def restore_mic_icon(self):
        self.toolbar.mic_btn.config(image=self.mic_icon)
        self.toolbar.mic_btn.image = self.mic_icon

    def activate_commands(self):
        threading.Thread(target=self.voice_commands, daemon=True).start()
        self.toolbar.mic_btn.config(image=self.mic_listening_icon)
        self.toolbar.mic_btn.image = self.mic_listening_icon
        self.display_feedback_safe("I'm here, dear. What can I do for you?")

    def start_listening(self):
        threading.Thread(target=self.listen_for_commands, daemon=True).start()

    def listen_for_commands(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Say 'Honey' to activate commands...")
            while True:
                try:
                    audio_data = r.listen(source)
                    text = r.recognize_google(audio_data).lower()
                    print(text)
                    if "honey" in text:
                        print("Wake word detected")
                        self.toolbar.mic_btn.config(image=self.mic_listening_icon)
                        self.display_feedback_safe("Yes, dear?")
                        self.voice_commands()
                        self.toolbar.mic_btn.config(image=self.mic_icon)
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    print(f"Speech recognition error: {e}")

    def voice_commands(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio_data = r.listen(source, timeout=5)
                command_text = r.recognize_google(audio_data).lower()
                self.display_feedback_safe(f"Okay, dear. Let me quickly do that for you... ({command_text})")

                # Calculator interaction
                if self.is_calculator_active == 1:
                    if "calculator" in command_text:
                        self.toolbar.commands["toggle_calculator"]()
                    else:
                        self.calculator.set_input_from_string(command_text)

                elif "new file please" in command_text:
                    self.toolbar.commands["new_file"]()
                elif "existing file please" in command_text or "abrihi" in command_text:
                    self.toolbar.commands["open_file"]()
                elif "save please" in command_text:
                    self.toolbar.commands["save"]()
                elif "save as please" in command_text or "save us please" in command_text:
                    self.toolbar.commands["save_as"]()
                elif "copy please" in command_text:
                    self.toolbar.commands["copy"]()
                elif "cut please" in command_text:
                    self.toolbar.commands["cut"]()
                elif "paste please" in command_text:
                    self.toolbar.commands["paste"]()
                elif "undo please" in command_text:
                    self.toolbar.commands["undo"]()
                elif "redo please" in command_text:
                    self.toolbar.commands["redo"]()
                elif "dark mode please" in command_text or "dark" in command_text:
                    if not self.is_dark_mode:
                        self.is_dark_mode = not self.is_dark_mode
                        self.toolbar.commands["toggle_theme"]()
                elif "light mode please" in command_text or "open the curtains please" in command_text:
                    if self.is_dark_mode:
                        self.is_dark_mode = not self.is_dark_mode
                        self.toolbar.commands["toggle_theme"]()
                #elif "minimize please" in command_text:
                    #self.toolbar.commands["minimize"]()
                elif command_text in ["exit please", "shut up", "avada kedavra", "yamete"]:
                    apps.shutdown()
                elif "open editor" in command_text:
                    self.toolbar.commands["toggleEditor"]()
                elif"open simulation" in command_text:
                    apps.open_simulator()
                    print("hello")
                elif"close simulation" in command_text:
                    apps.close_simulator()
                elif"open calculator" in command_text:
                    apps.open_calculator()
                elif"open camera" in command_text:
                    apps.open_camera()
                elif"close camera" in command_text:
                    apps.close_camera()
                elif"close calculator" in command_text:
                    apps.close_calculator()
                elif"take a picture" in command_text:
                    apps.take_picture()
                elif"close editor" in command_text:
                    self.toolbar.commands["closeEditor"]()

            except sr.WaitTimeoutError:
                self.display_feedback_safe("You were a little quiet, dear. Try again?")
            except sr.UnknownValueError:
                self.display_feedback_safe("I couldn't quite catch that, dear.")
            except sr.RequestError as e:
                self.display_feedback_safe(f"Oops. Something's wrong with the voice service. ({e})")
            except KeyError as e:
                self.display_feedback_safe(f"I didn't find a command for '{e}'.")
            except Exception as e:
                self.display_feedback_safe(f"Sorry, dear. I didn't quite get that... ({str(e)})")

            self.restore_mic_icon()
