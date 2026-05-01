import tkinter as tk
import threading
from src.compiler.Compiler import Compiler
import subprocess
import re
import time

class Menu(tk.Menu):
    def __init__(self, parent, text_editor, video_player, console_view, on_compile = None):
        super().__init__(parent)
        self.video_player = video_player
        self.text_editor = text_editor
        self.on_compile = on_compile
        self.console_view = console_view

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
        self.add_command(label="Clear Console", command=self.clear_console)
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
        start_time = time.time()

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

        total_duration = compiler.duration

        for line in process.stderr:
            print(line, end="")

            t = self.extract_time(line)
            if t is None or t <= 0:
                continue

            progress = (t / total_duration) * 100

            elapsed = time.time() - start_time
            speed = t / elapsed if elapsed > 0 else 0

            remaining_video = total_duration - t

            if speed > 0:
                eta_seconds = remaining_video / speed
            else:
                eta_seconds = 0

            eta_str = self.format_time(eta_seconds)

            message = f"Rendering... {progress:.1f}% | ETA: {eta_str}"

            self.after(0, lambda msg=message: self.video_player.file_label.config(text=msg))

        process.wait()

        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command)

        if self.on_compile:
            self.on_compile(compiler.layers)

        print("Rendered DVEL video to " + output_path + ".")
        self.after(0, lambda: self.load_and_play(output_path))

    def format_time(self, seconds):
        seconds = int(seconds)
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)

        if h > 0:
            return f"{h}:{m:02}:{s:02}"
        else:
            return f"{m:02}:{s:02}"

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

    def clear_console(self):
        self.console_view.clear()