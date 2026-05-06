import tkinter as tk
from ui.TextEditor import TextEditor
from ui.VideoPlayer import VideoPlayer
from ui.ConsoleView import ConsoleView
from ui.Menu import Menu
from ui.TimelineView import TimelineView
from ui.Theme import Theme
from tkinter import ttk
import os
import sys

class Window:
    def __init__(self):
        self.root = tk.Tk()

    def __create_window(self):
        self.root.title("DVEL")
        self.root.geometry("800x600")
        self.__maximize_window()
        style = self.__apply_dark_theme()
        self.root.configure(bg=Theme.BG)

        self.icon = tk.PhotoImage(file=self.resource_path("ui/DVEL_Icon.png"))
        self.root.iconphoto(True, self.icon)

    def resource_path(self, relative_path):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
        
    def __maximize_window(self):
        try:
            self.root.state("zoomed")  # Windows
        except:
            self.root.attributes("-zoomed", True)

    def __apply_dark_theme(self):
        style = ttk.Style()
        style.theme_use("clam")
        thumb = Theme.PANEL
        bg = Theme.BG
        panel = Theme.PANEL
        border = Theme.BORDER
        text = Theme.PANEL

        style.configure(
            "Vertical.TScrollbar",
            gripcount=0,
            background=thumb,
            troughcolor=bg,
            bordercolor=border,
            arrowcolor=text,
        )

        style.configure(
            "Horizontal.TScrollbar",
            gripcount=0,
            background=thumb,
            troughcolor=bg,
            bordercolor=border,
            arrowcolor=text,
        )
        style.configure(
            "Horizontal.TScale",
            gripcount=0,
            background=thumb,
            troughcolor=bg,
            bordercolor=border,
        )

        return style


    def __create_menu(self):
        self.menu = Menu(self.root, self.editor, self.video_player, self.console, on_compile = self.__refresh_timeline)
        self.root.config(menu=self.menu)

    def __window_layout(self):
        self.main_pane = tk.PanedWindow(
            self.root,
            orient="horizontal",
            sashrelief="raised",
            showhandle=True,
        )
        self.main_pane.pack(fill="both", expand=True)

        self.left_pane = tk.PanedWindow(
            self.main_pane,
            orient="vertical",
            sashrelief="raised",
            showhandle=True,
            bg=Theme.PANEL,
        )
        self.main_pane.add(self.left_pane, minsize=200)

        self.top_left_frame = tk.Frame(self.left_pane ,bg=Theme.PANEL)
        self.left_pane.add(self.top_left_frame, minsize=200, width=650, height=400)

        self.bottom_left_frame = tk.Frame(self.left_pane ,bg=Theme.PANEL)
        self.left_pane.add(self.bottom_left_frame, minsize=200)

        self.right_pane = tk.PanedWindow(
            self.main_pane,
            orient="vertical",
            sashrelief="raised",
            showhandle=True,
            bg=Theme.PANEL,
        )
        self.main_pane.add(self.right_pane, minsize=200)

        self.top_right_frame = tk.Frame(self.right_pane, bg=Theme.PANEL)
        self.right_pane.add(self.top_right_frame, minsize=150, height=300)

        self.bottom_right_frame = tk.Frame(self.right_pane, bg=Theme.PANEL)
        self.right_pane.add(self.bottom_right_frame, minsize=50)

    def __text_editor_view(self):
        self.top_left_frame.rowconfigure(0, weight=1)
        self.top_left_frame.columnconfigure(0, weight=1)

        self.editor = TextEditor(self.top_left_frame)
        self.editor.TextEditorView()
    
    def __timeline_view(self):
        self.timeline_view = TimelineView(self.bottom_left_frame, {}, scale=10)
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

    def __video_display_view(self):
        self.top_right_frame.rowconfigure(0, weight=1)
        self.top_right_frame.columnconfigure(0, weight=1)

        self.video_player = VideoPlayer(self.top_right_frame)

    def __console_view(self):
        self.bottom_right_frame.rowconfigure(0, weight=1)
        self.bottom_right_frame.columnconfigure(0, weight=1)

        self.console = ConsoleView(self.bottom_right_frame)
        self.console.console_view()

    def run(self):
        self.__create_window()
        self.__window_layout()
        self.__text_editor_view()
        self.__timeline_view()
        self.__video_display_view()
        self.__console_view()
        self.__create_menu()
        self.root.mainloop()