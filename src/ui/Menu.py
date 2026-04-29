import tkinter as tk
from src.compiler.Compiler import Compiler
import subprocess

class Menu(tk.Menu):
    def __init__(self, parent, text_editor, on_compile = None):
        super().__init__(parent)

        self.text_editor = text_editor
        self.on_compile = on_compile

        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="Open", command=self.open)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Save As", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        self.add_cascade(label="File", menu=file_menu)
        self.add_command(label="Compile", command=self.compile)
        self.add_command(label="Help", command=self.help)
        parent.config(menu=self)

    def open(self):
        self.text_editor.open_file()

    def compile(self):
        content = self.text_editor.get_content()
        compiler = Compiler()
        command = compiler.compile(content)
        subprocess.run(command, shell=True)
        if self.on_compile:
            self.on_compile(compiler.layers)

    def save(self):
        self.text_editor.save_file()

    def save_as(self):
        self.text_editor.save_file_as()

    def help(self):
        # Route to documentation
        print("Routing to documentation...")