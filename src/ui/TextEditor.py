import tkinter as tk

# blue window in left half of screen with text editor.
class TextEditor:
    def __init__(self, parent):
        self.parent = parent

    def TextEditorView(self):
        self.main_frame = tk.Frame(self.parent, bg="white")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)

        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        self._lineNumbers()
        self._scrollbar()
        

    def _lineNumbers(self):  
        self.line_numbers = tk.Text(
            self.main_frame,
            width=4,
            padx=4,
            takefocus=0,
            border=0,
            background="lightgray",
            state="disabled",
            font=("Courier", 12),
            wrap="none",
        )
        self.line_numbers.grid(row=0, column=0, sticky="ns")

        # Main text editor
        self.text_editor = tk.Text(
            self.main_frame,
            font=("Courier", 12),
            wrap="none",
            undo=True,
        )
        self.text_editor.grid(row=0, column=1, sticky="nsew")

    def _scrollbar(self):
        self.scrollbar = tk.Scrollbar(
            self.main_frame,
            orient="vertical",
            command=self.on_scroll,
        )
        self.scrollbar.grid(row=0, column=2, sticky="ns")

        self.text_editor.config(yscrollcommand=self.on_textscroll)
        #self.text_editor.insert("1.0", "# Start typing here...\n")

        self.status_bar = tk.Label(
            self.main_frame,
            text="Ln 1 | Col 1 | Words: 0",
            anchor="w",
            padx=6,
            font=("Courier", 10),
            bg="lightgray",
            fg="black",
        )
        self.status_bar.grid(row=1, column=0, columnspan=3, sticky="we")

        self.text_editor.tag_configure("current_line", background="")

        # Update line numbers when typing, clicking, scrolling, etc.
        self.text_editor.bind("<KeyRelease>", self.on_update)
        self.text_editor.bind("<MouseWheel>", self.on_update)
        self.text_editor.bind("<Button-1>", self.on_update)
        self.text_editor.bind("<Return>", self.on_update)
        self.text_editor.bind("<BackSpace>", self.on_update)

        # Linux scroll support
        self.text_editor.bind("<Button-4>", self.on_update)
        self.text_editor.bind("<Button-5>", self.on_update)

        self.update_line_numbers()

    def on_update(self, event=None):
        self.update_line_numbers()
        self.highlight_current_line()
        self.update_status_bar()

    def highlight_current_line(self):
        self.text_editor.tag_remove("current_line", "1.0", "end")
        self.text_editor.tag_add("current_line", "insert linestart", "insert lineend+1c")

    def update_line_numbers(self, event=None):
        line_count = int(self.text_editor.index("end-1c").split(".")[0])
        line_numbers_string = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", line_numbers_string)
        self.line_numbers.config(state="disabled")

        # Keep line numbers vertically aligned with text editor
        self.line_numbers.yview_moveto(self.text_editor.yview()[0])
    
    def update_status_bar(self):
        cursor_position = self.text_editor.index("insert")
        line, column = cursor_position.split(".")
        column = int(column) + 1

        content = self.text_editor.get("1.0", "end-1c")
        words = len(content.split()) if content.strip() else 0

        self.status_bar.config(
            text=f"Ln {line} | Col {column} | Words: {words}"
        )

    def on_scroll(self, *args):
        self.text_editor.yview(*args)
        self.line_numbers.yview(*args)

    def on_textscroll(self, *args):
        self.scrollbar.set(*args)
        self.line_numbers.yview_moveto(args[0])

    def get_content(self):
        content = self.text_editor.get("1.0", "end-1c")
        return content