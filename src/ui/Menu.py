import tkinter as tk
import subprocess
import threading
from src.compiler.Compiler import Compiler
import subprocess
import re

class Menu(tk.Menu):
    def __init__(self, parent, text_editor, video_player, on_compile = None):
        super().__init__(parent)
        self.video_player = video_player
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
        self.add_command(label="Render", command=self.render)
        self.add_command(label="Help", command=self.help)
        parent.config(menu=self)

    def open(self):
        self.text_editor.open_file()

    def compile(self):
        content = self.text_editor.get_content()
        compiler = Compiler()
        command = compiler.compile(content)
        if self.on_compile:
            self.on_compile(compiler.layers)

    def render(self):
        threading.Thread(target=self.render_task, daemon=True).start()

    def render_task(self):
        compiler = Compiler()
        content = self.text_editor.get_content()
        command = compiler.compile(content)
        output_path = compiler.parser.render_settings.export_path
        process: subprocess.Popen[str] = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        total_duration = 60 #need to change

        for line in process.stderr:
            t = self.extract_time(line)
            if t is not None:
                progress = (t / total_duration) * 100
                print(f"Progress: {t:.1f}%")

        process.wait()

        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command)
        if self.on_compile:
            self.on_compile(compiler.layers)

        print("Rendered DVEL video to " + output_path + ".")
        self.after(0, lambda: self.load_and_play(output_path))

    def extract_time(self, line):
        match = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", line)
        if match:
            h, m, s = match.groups()
            return int(h) * 3600 + int(m) * 60 + float(s)
        return None

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