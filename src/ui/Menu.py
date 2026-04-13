import tkinter as tk
from src.compiler.Compiler import compile_code

class Menu(tk.Menu):
    def __init__(self, parent, text_editor):
        super().__init__(parent)

        menu = tk.Menu(self)

        self.text_editor = text_editor

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Open", command=self.open)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        self.add_cascade(label="File", menu=file_menu)
        self.add_command(label="Compile", command=self.compile)
        self.add_command(label="Help", command=self.help)

    def open(self):
        # Route to open function
        print("Opening...")

    def compile(self):
        content = self.text_editor.get_content()
        compile_code(content)

    def save(self):
        # Route to save function here
        print("Saving...")

    def help(self):
        # Route to help function here
        print("Helping...")