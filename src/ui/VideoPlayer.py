import tkinter as tk
import vlc
import os
import sys
from tkinter import filedialog
from tkinter import ttk

class VideoPlayer:
    def __init__(self, parent_frame):
        vlc_path = self.get_vlc_path()

        os.environ["PATH"] = vlc_path + ";" + os.environ.get("PATH", "")

        self.instance = vlc.Instance([
            f"--plugin-path={os.path.join(vlc_path, 'plugins')}"
        ])

        self.player = self.instance.media_player_new()

        self.parent_frame = parent_frame
        self.parent_frame.rowconfigure(0, weight=1)
        self.parent_frame.rowconfigure(1, weight=0)
        self.parent_frame.rowconfigure(2, weight=0)
        self.parent_frame.rowconfigure(3, weight=0)
        self.parent_frame.columnconfigure(0, weight=1)

        self.video_widget = None
        self.status_label = None
        self.time_label = None
        self.progress_scale = None

        self.play_button = None
        self.pause_button = None
        #self.load_button = None
        self.stop_button = None

        self.is_dragging_progress = False

        self.build_ui()
        self.parent_frame.after(100, self.set_video_output)
        self.parent_frame.after(200, self.update_progress)

    def get_vlc_path(self):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, "vlc")

    def build_ui(self):
        self.video_widget = tk.Frame(self.parent_frame, bg="black")
        self.video_widget.grid(row=0, column=0, sticky="nsew")

        controls_frame = tk.Frame(self.parent_frame)
        controls_frame.grid(row=1, column=0, sticky="ew")

        controls_frame.columnconfigure(0, weight=1)
        controls_frame.columnconfigure(1, weight=1)
        controls_frame.columnconfigure(2, weight=1)
        controls_frame.columnconfigure(2, weight=1)

        #self.load_button = tk.Button(controls_frame, text="Load", command=self.pick_file)
        #self.load_button.grid(row=0, column=0, sticky="ew")

        self.play_button = tk.Button(controls_frame, text="Play", command=self.play)
        self.play_button.grid(row=0, column=0, sticky="ew")

        self.pause_button = tk.Button(controls_frame, text="Pause", command=self.pause)
        self.pause_button.grid(row=0, column=1, sticky="ew")

        self.stop_button = tk.Button(controls_frame, text="Stop", command=self.stop)
        self.stop_button.grid(row=0, column=2, sticky="ew")

        progress_frame = tk.Frame(self.parent_frame)
        progress_frame.grid(row=2, column=0, sticky="ew")
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.columnconfigure(1, weight=0)
        progress_frame.columnconfigure(2, weight=0)

        self.progress_scale = ttk.Scale(progress_frame, from_=0, to=1000, orient="horizontal")
        self.progress_scale.grid(row=0, column=0, sticky="ew", padx=(5, 5))

        self.progress_scale.bind("<Button-1>", self.on_progress_press)
        self.progress_scale.bind("<ButtonRelease-1>", self.on_progress_release)

        self.time_label = tk.Label(progress_frame, text="00:00 / 00:00", width=12, anchor="e")
        self.time_label.grid(row=0, column=1, sticky="e", padx=(0, 5))

        self.file_label = tk.Label(progress_frame, text="No video loaded", width=20, anchor="w")
        self.file_label.grid(row=0, column=2, sticky="w", padx=(0, 5))

    def set_video_output(self):
        self.video_widget.update_idletasks()
        window_id = self.video_widget.winfo_id()

        #The line below seems to only work on windows (line needed to map the video to the app window)
        self.player.set_hwnd(window_id)

    def pick_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a video file",
            filetypes=[
                ("Video Files", "*.mp4 *.avi *.mkv *.mov *.wmv"),
                ("All Files", "*.*")
            ]
        )

        if file_path:
            self.load(file_path)

    def load(self, file_path):
        media = self.instance.media_new(file_path)
        self.player.set_media(media)
        self.progress_scale.set(0)
        self.time_label.config(text="00:00 / 00:00")
        self.file_label.config(text=os.path.basename(file_path))

    def play(self):
        if self.player.get_media() is None:
            return

        self.set_video_output()
        self.player.play()
        #self.file_label.config(text="Playing")

    def pause(self):
        if self.player.get_media() is None:
            return

        self.player.pause()
        #self.file_label.config(text="Paused")

    def stop(self):
        if self.player.get_media() is None:
            return

        self.player.stop()
        self.progress_scale.set(0)
        self.time_label.config(text="00:00 / 00:00")
        #self.file_label.config(text="Stopped")

    def on_progress_press(self, event):
        self.is_dragging_progress = True

    def on_progress_release(self, event):
        if self.player.get_media() is None:
            self.is_dragging_progress = False
            return

        length = self.player.get_length()
        if length > 0:
            percent = self.progress_scale.get() / 1000.0
            new_time = int(length * percent)
            self.player.set_time(new_time)

        self.is_dragging_progress = False

    def update_progress(self):
        if self.player.get_media() is not None and not self.is_dragging_progress:
            length = self.player.get_length()
            current_time = self.player.get_time()

            if length > 0 and current_time >= 0:
                percent = current_time / length
                self.progress_scale.set(percent * 1000)

                current_text = self.format_time(current_time)
                total_text = self.format_time(length)
                self.time_label.config(text=f"{current_text} / {total_text}")

        self.parent_frame.after(200, self.update_progress)

    def format_time(self, milliseconds):
        total_seconds = max(0, milliseconds // 1000)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02}:{seconds:02}"