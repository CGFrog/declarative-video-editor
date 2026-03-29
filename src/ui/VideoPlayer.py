import tkinter as tk
from tkVideoPlayer import TkinterVideo

class VideoPlayer:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame

        self.parent_frame.rowconfigure(0, weight=1)
        self.parent_frame.rowconfigure(1, weight=0)
        self.parent_frame.columnconfigure(0, weight=1)

        self.video_widget = None
        self.status_label = None
        self.play_button = None
        self.pause_button = None
        self.stop_button = None

        self.build_ui()

    def build_ui(self):
        if TkinterVideo is None:
            self.status_label = tk.Label(
                self.parent_frame,
                text="tkVideoPlayer is not installed."
            )
            self.status_label.grid(row=0, column=0, sticky="nsew")
            return

        self.video_widget = TkinterVideo(self.parent_frame, scaled=True)
        self.video_widget.grid(row=0, column=0, sticky="nsew")

        controls_frame = tk.Frame(self.parent_frame)
        controls_frame.grid(row=1, column=0, sticky="ew")

        controls_frame.columnconfigure(0, weight=1)
        controls_frame.columnconfigure(1, weight=1)
        controls_frame.columnconfigure(2, weight=1)

        self.play_button = tk.Button(controls_frame, text="Play", command=self.play)
        self.play_button.grid(row=0, column=0, sticky="ew")

        self.pause_button = tk.Button(controls_frame, text="Pause", command=self.pause)
        self.pause_button.grid(row=0, column=1, sticky="ew")

        self.stop_button = tk.Button(controls_frame, text="Stop", command=self.stop)
        self.stop_button.grid(row=0, column=2, sticky="ew")

    def load(self, file_path):
        if self.video_widget is not None:
            self.video_widget.load(file_path)

    def play(self):
        if self.video_widget is not None:
            self.video_widget.play()

    def pause(self):
        if self.video_widget is not None:
            self.video_widget.pause()

    def stop(self):
        if self.video_widget is not None:
            self.video_widget.stop()