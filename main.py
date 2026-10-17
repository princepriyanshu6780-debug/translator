import sys
import threading
import time
import tkinter as tk
from tkinter import scrolledtext

from translator import speak, listen, translate_to_hindi


class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎙️ English → Hindi Voice Translator")
        self.root.geometry("650x520")
        self.root.configure(bg="#1e1e2e")

        self.running = False
        self.thread = None

        self.build_ui()

    def build_ui(self):
        # Title
        title = tk.Label(
            self.root,
            text="🎙️ English → Hindi Voice Translator",
            font=("Arial", 16, "bold"),
            bg="#1e1e2e", fg="#f9e2af", pady=10
        )
        title.pack()

        # Status
        self.status_label = tk.Label(
            self.root,
            text="Status: Idle",
            font=("Arial", 11),
            bg="#1e1e2e", fg="#a6e3a1"
        )
        self.status_label.pack(pady=5)

        # English box
        tk.Label(self.root, text="👤 You said (English):",
                 bg="#1e1e2e", fg="#cdd6f4", font=("Arial", 11, "bold")).pack(anchor="w", padx=15)
        self.english_box = scrolledtext.ScrolledText(
            self.root, height=7, wrap=tk.WORD,
            bg="#313244", fg="#cdd6f4", font=("Arial", 11),
            insertbackground="white"
        )
        self.english_box.pack(padx=15, pady=5, fill="x")

        # Hindi box
        tk.Label(self.root, text="🇮🇳 Translation (Hindi):",
                 bg="#1e1e2e", fg="#cdd6f4", font=("Arial", 11, "bold")).pack(anchor="w", padx=15)
        self.hindi_box = scrolledtext.ScrolledText(
            self.root, height=7, wrap=tk.WORD,
            bg="#313244", fg="#f5c2e7", font=("Arial", 11),
            insertbackground="white"
        )
        self.hindi_box.pack(padx=15, pady=5, fill="x")

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(pady=15)

        self.start_btn = tk.Button(
            btn_frame, text="▶️ ON  (Start)", command=self.start_app,
            bg="#89b4fa", fg="#1e1e2e", font=("Arial", 12, "bold"),
            padx=25, pady=10, relief="flat", cursor="hand2"
        )
        self.start_btn.pack(side="left", padx=10)

        self.stop_btn = tk.Button(
            btn_frame, text="⏹️ OFF (Stop)", command=self.stop_app,
            bg="#45475a", fg="#888", font=("Arial", 12, "bold"),
            padx=25, pady=10, relief="flat", state="disabled", cursor="hand2"
        )
        self.stop_btn.pack(side="left", padx=10)

    def start_app(self):
        self.start_btn.config(state="disabled", bg="#45475a")
        self.stop_btn.config(state="normal", bg="#f38ba8", fg="#1e1e2e")

        self.thread = threading.Thread(target=self.run_worker, daemon=True)
        self.thread.start()

    def run_worker(self):
        self.update_status("🔊 Greeting...")
        speak("Hello, I am an English to Hindi translator. Today how can I help you?", lang='en')

        self.running = True
        while self.running:
            self.update_status("🎤 Listening...")
            english_text = listen()

            if english_text:
                self.update_status("🔄 Translating...")
                hindi_text = translate_to_hindi(english_text)

                if hindi_text:
                    self.update_output(english_text, hindi_text)
                    self.update_status("🔊 Speaking Hindi...")
                    speak(hindi_text, lang='hi')

            time.sleep(0.3)

    def update_output(self, english, hindi):
        self.english_box.insert(tk.END, english + "\n")
        self.english_box.see(tk.END)

        self.hindi_box.insert(tk.END, hindi + "\n")
        self.hindi_box.see(tk.END)

    def update_status(self, text):
        self.status_label.config(text=f"Status: {text}")

    def stop_app(self):
        self.running = False
        self.start_btn.config(state="normal", bg="#89b4fa", fg="#1e1e2e")
        self.stop_btn.config(state="disabled", bg="#45475a", fg="#888")
        self.update_status("Stopped ⏹️")


if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()