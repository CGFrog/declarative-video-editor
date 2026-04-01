import tkinter as tk
import vlc

class VideoPlayer:
    def __init__(self, parent_frame):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

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
        self.video_widget = tk.Frame(self.parent_frame, bg="black")
        self.video_widget.grid(row=0, column=0, sticky="nsew")

        # SOLUTION ONLY WORKS ON WINDOWS RN

        controls_frame = tk.Frame(self.parent_frame)
        controls_frame.grid(row=1, column=0, sticky="ew")

        controls_frame.columnconfigure(0, weight=1)
        controls_frame.columnconfigure(1, weight=1)
        controls_frame.columnconfigure(2, weight=1)

        #self.player.set_hwnd(controls_frame.winfo_id())

        self.play_button = tk.Button(controls_frame, text="Play", command=self.play)
        self.play_button.grid(row=0, column=0, sticky="ew")

        self.pause_button = tk.Button(controls_frame, text="Pause", command=self.pause)
        self.pause_button.grid(row=0, column=1, sticky="ew")

        self.stop_button = tk.Button(controls_frame, text="Stop", command=self.stop)
        self.stop_button.grid(row=0, column=2, sticky="ew")

    def load(self, file_path):
        media = self.instance.media_new(file_path)
        self.player.set_media(media)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()