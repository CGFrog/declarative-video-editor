import tkinter as tk
from .VideoPlayer import VideoPlayer

class Window:
    def __init__(self):
        self.root = tk.Tk()
        pass

    def createWindow(self):
        self.root.title("Declarative Video Editor")
        self.root.geometry("400x300")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

    def windowLayout(self):
        self.main_frame = tk.Frame(self.root, bg="YELLOW")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.rowconfigure(0, weight=1, uniform="rows")
        self.main_frame.rowconfigure(1, weight=1, uniform="rows")
        self.main_frame.columnconfigure(0, weight=1, uniform="cols")
        self.main_frame.columnconfigure(1, weight=1, uniform="cols")

    def textEditorView(self):
        self.left_frame = tk.Frame(self.main_frame, bg="BLUE")
        self.left_frame.grid(row=0, rowspan=2, column=0, sticky="nsew")
        # create and initialize text box and other elements from textEditor class

    def videoDisplayView(self):
        self.right_frame = tk.Frame(self.main_frame, bg="GREEN")
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        # create and initialize media player and other elements from videoPlayer class
        self.video_player = VideoPlayer(self.right_frame)

    def consoleView(self):
        self.bottom_frame = tk.Frame(self.main_frame, bg="RED")
        self.bottom_frame.grid(row=1, column=1, sticky="nsew")
        # create and initialize console and other elements from console class

    def run(self):
        self.createWindow()
        self.windowLayout()
        self.textEditorView()
        self.videoDisplayView()
        self.consoleView()
        self.root.mainloop()