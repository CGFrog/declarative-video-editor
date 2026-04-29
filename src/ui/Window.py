import tkinter as tk
import sv_ttk
from src.ui.TextEditor import TextEditor
from src.ui.VideoPlayer import VideoPlayer
from src.ui.ConsoleView import ConsoleView
from src.ui.Menu import Menu
from src.ui.TimelineView import TimelineView
from src.ui.Theme import Theme

class Window:
    def __init__(self):
        self.root = tk.Tk()

    def create_window(self):
        self.root.title("Declarative Video Editor")
        self.root.geometry("800x600")
        self.root.configure(bg=Theme.BG)

    def create_menu(self):
        self.menu = Menu(self.root, self.editor, on_compile = self.__refresh_timeline)
        self.root.config(menu=self.menu)

    def window_layout(self):
        self.main_pane = tk.PanedWindow(
            self.root,
            orient="horizontal",
            sashrelief="raised",
            showhandle=True,
        )
        self.main_pane.pack(fill="both", expand=True)

        self.left_frame = tk.Frame(self.main_pane,bg=Theme.PANEL)
        self.main_pane.add(self.left_frame, minsize=200)

        self.right_pane = tk.PanedWindow(
            self.main_pane,
            orient="vertical",
            sashrelief="raised",
            showhandle=True,
            bg=Theme.PANEL,
        )
        self.main_pane.add(self.right_pane, minsize=200)

        self.top_right_frame = tk.Frame(self.right_pane, bg=Theme.PANEL)
        self.right_pane.add(self.top_right_frame, minsize=150)

        self.bottom_right_frame = tk.Frame(self.right_pane, bg=Theme.PANEL)
        self.right_pane.add(self.bottom_right_frame, minsize=100)

    def text_editor_view(self):
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

    def video_display_view(self):
        self.top_right_frame.rowconfigure(0, weight=1)
        self.top_right_frame.columnconfigure(0, weight=1)

        self.video_player = VideoPlayer(self.top_right_frame)


    def console_view(self):
        self.bottom_right_frame.rowconfigure(0, weight=1)
        self.bottom_right_frame.columnconfigure(0, weight=1)

        self.console = ConsoleView(self.bottom_right_frame)
        self.console.console_view()
        self.console.set_input_callback(self.console.handle_console_input)


    def run(self):
        self.create_window()
        self.window_layout()
        self.text_editor_view()
        self.__timeline_view()
        self.video_display_view()
        self.console_view()
        self.create_menu()
        self.root.mainloop()