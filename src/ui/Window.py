import tkinter as tk
from src.ui.TextEditor import TextEditor
from src.ui.VideoPlayer import VideoPlayer
from src.ui.ConsoleView import ConsoleView
from src.ui.Menu import Menu
from src.ui.TimelineView import TimelineView

class Window:
    def __init__(self):
        self.root = tk.Tk()

    def createWindow(self):
        self.root.title("Declarative Video Editor")
        self.root.geometry("800x600")

    def createMenu(self):
        self.menu = Menu(self.root, self.editor, on_compile = self.__refresh_timeline)
        self.root.config(menu=self.menu)

    def windowLayout(self):
        self.main_pane = tk.PanedWindow(
            self.root,
            orient="horizontal",
            sashrelief="raised",
            showhandle=True,
        )
        self.main_pane.pack(fill="both", expand=True)

        self.left_frame = tk.Frame(self.main_pane)
        self.main_pane.add(self.left_frame, minsize=200)

        self.right_pane = tk.PanedWindow(
            self.main_pane,
            orient="vertical",
            sashrelief="raised",
            showhandle=True,
        )
        self.main_pane.add(self.right_pane, minsize=200)

        self.top_right_frame = tk.Frame(self.right_pane)
        self.right_pane.add(self.top_right_frame, minsize=150)

        self.bottom_right_frame = tk.Frame(self.right_pane)
        self.right_pane.add(self.bottom_right_frame, minsize=100)

    def TextEditorView(self):
        self.left_frame.rowconfigure(0, weight=1)
        self.left_frame.columnconfigure(0, weight=1)

        self.editor = TextEditor(self.left_frame)
        self.editor.TextEditorView()
    
    def __timeline_view(self):
        self.timeline_view = TimelineView(self.left_frame, {}, scale=10)
        self.timeline_view._enable_timeline(row=1, column=0)
        self.timeline_view.canvas.bind("<Configure>", lambda e: self.timeline_view._draw_timeline())
    
    def __refresh_timeline(self, layers):
        if not any(layers.values()):
            return
        
        canvas_width = self.timeline_view.canvas.winfo_width()
        total_duration = max(
            clip.timeline_start + (clip.src_end - clip.src_start)
            for clips in layers.values()
            for clip in clips
        )
        self.timeline_view.scale = canvas_width / total_duration
        self.timeline_view.layers = layers
        self.timeline_view._draw_timeline()

    def videoDisplayView(self):
        self.top_right_frame.rowconfigure(0, weight=1)
        self.top_right_frame.columnconfigure(0, weight=1)

        self.video_player = VideoPlayer(self.top_right_frame)


    def consoleView(self):
        self.bottom_right_frame.rowconfigure(0, weight=1)
        self.bottom_right_frame.columnconfigure(0, weight=1)

        self.console = ConsoleView(self.bottom_right_frame)
        self.console.console_view()
        self.console.set_input_callback(self.console.handle_console_input)


    def run(self):
        self.createWindow()
        self.windowLayout()
        self.TextEditorView()
        self.__timeline_view()
        self.videoDisplayView()
        self.consoleView()
        self.createMenu()
        self.root.mainloop()