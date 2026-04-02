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
        self.load_button = None
        self.stop_button = None

        self.build_ui()
        self.parent_frame.after(100, self.setVideoOutput)

    def build_ui(self):
        self.video_widget = tk.Frame(self.parent_frame, bg="black")
        self.video_widget.grid(row=0, column=0, sticky="nsew")

        controls_frame = tk.Frame(self.parent_frame)
        controls_frame.grid(row=1, column=0, sticky="ew")

        controls_frame.columnconfigure(0, weight=1)
        controls_frame.columnconfigure(1, weight=1)
        controls_frame.columnconfigure(2, weight=1)
        controls_frame.columnconfigure(3, weight=1)

        #self.player.set_hwnd(controls_frame.winfo_id())

        self.play_button = tk.Button(controls_frame, text="Play", command=self.play)
        self.play_button.grid(row=0, column=0, sticky="ew")

        self.pause_button = tk.Button(controls_frame, text="Pause", command=self.pause)
        self.pause_button.grid(row=0, column=1, sticky="ew")

        self.load_button = tk.Button(controls_frame, text="Load", command=lambda: self.load("test.mp4"))
        self.load_button.grid(row=0, column=2, sticky="ew")

        self.stop_button = tk.Button(controls_frame, text="Stop", command=self.stop)
        self.stop_button.grid(row=0, column=3, sticky="ew")

        self.status_label = tk.Label(self.parent_frame, text="No video loaded", anchor="w")
        self.status_label.grid(row=2, column=0, sticky="ew")

    def setVideoOutput(self):
        self.video_widget.update_idletasks()
        window_id = self.video_widget.winfo_id()

        #The line below seems to only work on windows (line needed to map the video to the app window)
        self.player.set_hwnd(window_id)

    def load(self, file_path):
        media = self.instance.media_new(file_path)
        self.player.set_media(media)
        self.status_label.config(text=f"Loaded: {file_path}")

    def play(self):
        if self.player.get_media() is None:
            return

        self.player.play()
        self.status_label.config(text="Playing")

    def pause(self):
        if self.player.get_media() is None:
            return

        self.player.pause()
        self.status_label.config(text="Paused")

    def stop(self):
        if self.player.get_media() is None:
            return

        self.player.stop()
        self.status_label.config(text="Stopped")