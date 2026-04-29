import tkinter as tk
import os
from tkinter import ttk


HEIGHT = 40
PADDING = 10
OFFSET = 10
X_HEIGHT = 25
Y_WIDTH = 60


class TimelineView:
    def __init__(self, parent, layers: dict, scale=10):
        self.parent = parent
        self.layers = layers
        self.scale = scale

    def _enable_timeline(self, row=0, column=0):
        self.frame = tk.Frame(self.parent, bg="black")
        self.frame.grid(row=row, column=column, sticky="nsew")

        self.parent.rowconfigure(row, weight=1)
        self.parent.columnconfigure(column, weight=1)

        self.frame.rowconfigure(1, weight = 1)
        self.frame.columnconfigure(1, weight = 1)

        self.corner = tk.Frame(self.frame, bg="gray20", width=Y_WIDTH, height=X_HEIGHT)
        self.corner.grid(row=0, column=0, sticky="nsew")

        self.x_axis = tk.Canvas(self.frame, bg="gray20", height=X_HEIGHT, highlightthickness=0)
        self.x_axis.grid(row=0, column=1, sticky="ew")

        self.y_axis = tk.Canvas(self.frame, bg="gray20", width=Y_WIDTH, highlightthickness=0)
        self.y_axis.grid(row=1, column=0, sticky="ns")       

        self.canvas = tk.Canvas(self.frame, bg="gray15", height = 175)
        self.canvas.grid(row=1, column=1, sticky="nsew")

        self.scroll_x = ttk.Scrollbar(
            self.frame,
            orient="horizontal", 
            command=self._xview,
            style="Dark.Horizontal.TScrollbar"
        )
        self.scroll_x.grid(row=2, column=1, sticky="ew")

        self.scroll_y = ttk.Scrollbar(
            self.frame, 
            orient="vertical", 
            command=self._yview,
            style="Dark.Vertical.TScrollbar",
        )
        self.scroll_y.grid(row=1, column=2, sticky="ns")

        self.canvas.configure(
            xscrollcommand=self.scroll_x.set,
            yscrollcommand=self.scroll_y.set
        )
        
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)
        self.canvas.bind("<Button-5>", self._on_mousewheel)

        self._draw_timeline()

    def _on_mousewheel(self, event):
        if event.num == 4:
            self._yview("scroll", -1, "units")
        elif event.num == 5:
            self._yview("scroll", 1, "units")
        else:
            self._yview("scroll", int(-1 * (event.delta / 120)), "units")
    
    def _xview(self, *args):
        self.canvas.xview(*args)
        self.x_axis.xview(*args)

    def _yview(self, *args):
        self.canvas.yview(*args)
        self.y_axis.yview(*args)
    
    def _format_time(self, seconds):
        seconds = int(seconds)
        hrs = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60
        if hrs > 0:
            return f"{hrs:02}:{mins:02}:{secs:02}"
        return f"{mins:02}:{secs:02}"
    
    def __draw_x_label(self, content_width):
        self.x_axis.configure(scrollregion=(0, 0, content_width, X_HEIGHT)) 
        t = 0
        while t <= content_width:
            self.x_axis.create_line(t, X_HEIGHT - 5, t, X_HEIGHT, fill="white")
            time_label = self._format_time(t / self.scale)
            self.x_axis.create_text(t + 2, X_HEIGHT // 2, text=time_label, fill="white", anchor="w", font=("Courier", 8))
            t += 50
    
    def __draw_y_label(self, num_layers, content_height):
        self.y_axis.configure(scrollregion=(0, 0, Y_WIDTH, content_height))
        for z in range(num_layers):
            y = content_height - (z + 1) * (HEIGHT + PADDING) - PADDING
            mid_y = y + HEIGHT // 2
            self.y_axis.create_text(
                Y_WIDTH - 8, mid_y,
                text=f"Layer {z}",
                fill="white",
                anchor="e",
                font=("Courier", 9, "bold"),
            )
            self.y_axis.create_line(0, y, Y_WIDTH, y, fill="gray40")
    
    def __draw_clips(self, content_height, content_width):
        for z, clips in self.layers.items():
            y = content_height - (z + 1) * (HEIGHT + PADDING) - PADDING
            self.canvas.create_line(0, y, content_width, y, fill="white")
            
            for clip in clips:
                x1 = clip.timeline_start * self.scale
                x2 = x1 + (clip.src_end - clip.src_start) * self.scale
                self.canvas.create_rectangle(x1, y + 5, x2, y + 45, fill="blue")
                #would be better to have label be the name of video in code 
                label = os.path.splitext(os.path.basename(clip.path))[0]
                self.canvas.create_text(x1 + 4, y + 25, text=label, fill="white", anchor="w", font=("Courier", 9))
    
    def __generate_canvas_size(self):
        num_layers = max(self.layers.keys(), default = 0) + 1
        content_height = OFFSET + num_layers * (HEIGHT + PADDING) + PADDING

        content_width = max(
            (
                (clip.timeline_start + (clip.src_end - clip.src_start)) * self.scale
                for clips in self.layers.values()
                for clip in clips
            ),
            default = 0
        ) + self.scale + PADDING * 2

        content_width = max(content_width, self.canvas.winfo_width())
        content_height = max(content_height, self.canvas.winfo_height())

        return num_layers, content_width, content_height
        
    def _draw_timeline(self):
        self.canvas.delete("all")
        self.x_axis.delete("all")
        self.y_axis.delete("all")
    
        num_layers, content_width, content_height = self.__generate_canvas_size()
        self.__draw_x_label(content_width)
        self.__draw_y_label(num_layers, content_height)
        self.__draw_clips(content_height, content_width)
        

        self.frame.update_idletasks()
        self.canvas.configure(scrollregion=(0, 0, content_width, content_height))
