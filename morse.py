import json
from pynput import keyboard
import time
from threading import Timer
import pyautogui

class MorseCodeListener:
    def __init__(self):
        self.controll_key = keyboard.Key.ctrl_l
        self.morse_dict = {
            ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E", "..-.": "F", "--.": "G",
            "....": "H", "..": "I", ".---": "J", "-.-": "K", ".-..": "L", "--": "M", "-.": "N",
            "---": "O", ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T", "..-": "U",
            "...-": "V", ".--": "W", "-..-": "X", "-.--": "Y", "--..": "Z"
        }
        self.morse_actions = self.load_actions("actions.json")
        self.morse_activation = ".."
        self.last_release_time = 0
        self.dot_length = 0.2
        self.letter_space = 1
        self.current_morse = ""
        self.current_letter_timer = None
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        self.is_active = False

    def load_actions(self, filepath):
        with open(filepath, "r") as file:
            action_mappings = json.load(file)
        return action_mappings

    def on_press(self, key):
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            self.last_press_time = time.time()

    def on_release(self, key):
        if key == self.controll_key:
            duration = time.time() - self.last_press_time
            if duration < self.dot_length:
                self.add_letter(".")
            else:
                self.add_letter("-")

    def add_letter(self, letter):
        self.current_morse += letter

        if self.current_letter_timer is not None:
            self.current_letter_timer.cancel()
        self.current_letter_timer = Timer(self.letter_space, self.translate_morse)
        self.current_letter_timer.start()

    def translate_morse(self):
        if self.is_active:
            self.execute_action(self.current_morse)
            self.is_active = False
        elif self.current_morse == self.morse_activation:
            self.is_active = True
            print("Listening...", end='\n')

        self.current_morse = ""

    def execute_action(self, action_key):
        action = next((item for item in self.morse_actions if item["key"] == action_key), None)

        if action is None:
            print("Action not found:", action_key)
            return

        print("Executing action:", action["name"])
        pyautogui.press(action["action"])

    def run(self):
        try:
            self.listener.join()
        except KeyboardInterrupt:
            self.listener.stop()
            print("\nListener stopped.")

if __name__ == "__main__":
    morse_code_listener = MorseCodeListener()
    morse_code_listener.run()
