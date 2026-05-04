import tkinter as tk
from tkinter import ttk
from src.ui.Theme import Theme
import sys

class ConsoleView:
    def __init__(self,parent):
        self.parent = parent
        self.input_callback = None
        self.input_start_index = "1.0"
    
    def flush(self):
        pass

    def console_view(self):
        self.main_frame = tk.Frame(self.parent, bg=Theme.BG)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        self.__console_output()
        self.__redirect_Out()

    def __console_output(self):
        self.console = tk.Text(self.main_frame, bg=Theme.BG, fg="white", wrap="word", state="disabled")
        self.console.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(
            self.main_frame, 
            orient="vertical", 
            command=self.console.yview,
            style="Dark.Vertical.TScrollbar"    
        )
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.console.config(yscrollcommand=self.scrollbar.set)

    def __redirect_Out(self):
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

        self.parent.after(100, self._apply_redirect)

    def _apply_redirect(self):
        sys.stdout = self
        sys.stderr = self

        print(r"""
▓█████▄ ██▒   █▓▓█████  ██▓    
▒██▀ ██▌▓██░   █▒▓█   ▀ ▓██▒    
░██   █▌ ▓██  █▒░▒███   ▒██░    
░▓█▄   ▌  ▒██ █░░▒▓█  ▄ ▒██░    
░▒████▓   ▒▀█░  ░▒████▒░██████▒
▒▒▓  ▒   ░ ▐░  ░░ ▒░ ░░ ▒░▓  ░
░ ▒  ▒   ░ ░░   ░ ░  ░░ ░ ▒  ░
░ ░  ░     ░░     ░     ░ ░   
░         ░     ░  ░    ░  ░
░          ░                   
        """)
        
    def write(self, message):
        try:
            self.console.config(state="normal")
            self.console.insert("end", message)
            self.console.see("end")
            self.console.config(state="disabled")
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
    def clear(self):
        self.console.config(state="normal")
        self.console.delete("1.0", "end")
        self.console.config(state="disabled")
        print(r"""
        ▓█████▄ ██▒   █▓▓█████  ██▓    
        ▒██▀ ██▌▓██░   █▒▓█   ▀ ▓██▒    
        ░██   █▌ ▓██  █▒░▒███   ▒██░    
        ░▓█▄   ▌  ▒██ █░░▒▓█  ▄ ▒██░    
        ░▒████▓   ▒▀█░  ░▒████▒░██████▒
        ▒▒▓  ▒   ░ ▐░  ░░ ▒░ ░░ ▒░▓  ░
        ░ ▒  ▒   ░ ░░   ░ ░  ░░ ░ ▒  ░
        ░ ░  ░     ░░     ░     ░ ░   
        ░         ░     ░  ░    ░  ░
        ░          ░                   
                """)
