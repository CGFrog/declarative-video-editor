import tkinter as tk
import sys

class ConsoleView:
    def __init__(self,parent):
        self.parent = parent

    def ConsoleView(self):
        self.main_frame = tk.Frame(self.parent, bg="black")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        self.consoleOutput()
        self.redirectOut()

    def consoleOutput(self):
        self.console = tk.Text(self.main_frame, bg="black", fg="white", state="disabled", wrap="word")
        self.console.grid(row=0, column=0, stick="nsew")

        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.console.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.console.config(yscrollcommand=self.scrollbar.set)

    def redirectOut(self):
        sys.stdout = self
        sys.stderr = self

    def write(self, message):
        self.console.config(state="normal")
        self.console.insert("end", message)
        self.console.see("end")
        self.console.config(state="disabled")