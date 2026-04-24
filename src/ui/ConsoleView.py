import tkinter as tk
import sys

class ConsoleView:
    def __init__(self,parent):
        self.parent = parent
        self.input_callback = None
        self.input_start_index = "1.0"

    def console_view(self):
        self.main_frame = tk.Frame(self.parent, bg="black")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        self.consoleOutput()
        self.redirectOut()

    def consoleOutput(self):
        self.console = tk.Text(self.main_frame, bg="black", fg="white", wrap="word")
        self.console.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.console.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.console.bind("<Return>", self.on_enter)
        self.console.config(yscrollcommand=self.scrollbar.set)

    def redirectOut(self):
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

        self.parent.after(100, self._apply_redirect)

    def _apply_redirect(self):
        sys.stdout = self
        sys.stderr = self

        print("Welcome to DVEL!")

    def write(self, message):
        try:
            self.console.insert("end", message)
            self.console.see("end")
            self.input_start_index = self.console.index("end-1c")
        except Exception:
            self.original_stdout.write(message)

    def set_input_callback(self, callback):
        self.input_callback = callback

    def on_enter(self, event):
        input_text = self.console.get(self.input_start_index, "end-1c").strip()

        self.console.insert("end", "\n")
        self.console.see("end")

        if self.input_callback:
            self.input_callback(input_text)

        self.input_start_index = self.console.index("end-1c")

        return "break"

    def handle_console_input(self, text):
        print(f"You typed: {text}")