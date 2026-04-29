import tkinter as tk
import subprocess
import threading
from src.compiler.Compiler import Compiler

class Menu(tk.Menu):
    def __init__(self, parent, text_editor, video_player):
        super().__init__(parent)

        menu = tk.Menu(self)

        self.video_player = video_player
        self.text_editor = text_editor

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Open", command=self.open)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Save As", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        self.add_cascade(label="File", menu=file_menu)
        self.add_command(label="Compile", command=self.compile)
        self.add_command(label="Render", command=self.render)
        self.add_command(label="Help", command=self.help)

    def open(self):
        self.text_editor.open_file()

    def compile(self):
        content = self.text_editor.get_content()
        command = Compiler().compile(content)

    def render(self):
        threading.Thread(target=self.render_task, daemon=True).start()

    def render_task(self):
        compiler = Compiler()
        content = self.text_editor.get_content()
        command = compiler.compile(content)
        output_path = compiler.parser.render_settings.export_path
        subprocess.run(command, shell=True, check=True)
        print("--- Created: " + output_path + " ---")
        self.after(0, lambda: self.load_and_play(output_path))

    def load_and_play(self, path):
        self.video_player.load(path)
        self.after(100, self.video_player.play)


    def save(self):
        self.text_editor.save_file()

    def save_as(self):
        self.text_editor.save_file_as()

    def help(self):
        # Route to documentation
        print("Routing to documentation...")