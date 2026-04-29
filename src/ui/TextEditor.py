import tkinter as tk
from tkinter import filedialog, messagebox
from src.compiler.lexer.Lexer import Lexer
from src.compiler.lexer.Token import TokenLabel as TL
from src.ui.Theme import Theme
from tkinter import ttk

# blue window in left half of screen with text editor.
class TextEditor:
    def __init__(self, parent):
        self.parent = parent
        self.lexer = Lexer()
        self.current_file = None

    def TextEditorView(self):
        self.main_frame = tk.Frame(self.parent, bg=Theme.PANEL)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)

        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        self._lineNumbers()
        self._scrollbar()
        self._bind_shortcuts()
        self.update_status_bar()
        self.highlight_syntax()

    def _lineNumbers(self):  
        self.line_numbers = tk.Text(
            self.main_frame,
            width=4,
            padx=4,
            takefocus=0,
            border=0,
            background=Theme.PANEL,
            fg=Theme.MUTED,
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
            bg=Theme.BG,
            fg=Theme.TEXT,
            borderwidth=0,
            highlightthickness=0,
            insertbackground=Theme.CARET,
            selectbackground=Theme.SELECTION,
        )
        self.text_editor.grid(row=0, column=1, sticky="nsew")
        self._configure_syntax_tags()

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
            bg=Theme.PANEL,
            fg=Theme.MUTED,
        )
        self.status_bar.grid(row=1, column=0, columnspan=3, sticky="we")

        self.text_editor.tag_configure(
         "current_line",
        background=Theme.CURRENT_LINE
        )

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
        self.highlight_current_line()
        self.update_status_bar()

    def _bind_shortcuts(self):
        self.text_editor.bind("<Control-s>", self.save_file)
        self.text_editor.bind("<Control-o>", self.open_file)
        self.text_editor.bind("<Control-S>", self.save_file_as)

    def on_update(self, event=None):
        self.update_line_numbers()
        self.highlight_current_line()
        self.update_status_bar()

        if hasattr(self, "_highlight_after"):
            self.text_editor.after_cancel(self._highlight_after)

        self._highlight_after = self.text_editor.after(200, self.highlight_syntax)

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

        file_name = self.current_file if self.current_file else "Untitled"

        self.status_bar.config(
            text=f"{file_name} | Ln {line} | Col {column} | Words: {words}"
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
    def save_file(self, event=None):
        if self.current_file:
            try:
                with open(self.current_file, "w", encoding="utf-8") as f:
                    content = self.text_editor.get("1.0", "end-1c")
                    f.write(content)    
            except Exception as e:
                messagebox.showerror("Save File", f"Error saving file: {e}")
        else:
            self.save_file_as()

        return "break"  # Prevents default behavior

    def save_file_as(self, event=None):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".DVEL",
            filetypes=[("DVEL Files", "*.DVEL"), ("All Files", "*.*")],
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    content = self.text_editor.get("1.0", "end-1c")
                    f.write(content)
                self.current_file = file_path   
            except Exception as e:
                messagebox.showerror("Save File As", f"Error saving file: {e}")

        return "break"  # Prevent default behavior
    
    def open_file(self, event=None):
        file_path = filedialog.askopenfilename(
            filetypes=[("DVEL Files", "*.DVEL"), ("All Files", "*.*")],
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.text_editor.delete("1.0", "end")
                self.text_editor.insert("1.0", content)
                self.current_file = file_path
                self.update_line_numbers()
                self.update_status_bar()
                self.highlight_syntax()
            except Exception as e:
                messagebox.showerror("Open File", f"Error opening file: {e}")

        return "break"  # Prevent default behavior

    def _configure_syntax_tags(self):
        self.text_editor.tag_configure("media", foreground=Theme.S_MEDIA)
        self.text_editor.tag_configure("identifier", foreground=Theme.S_IDENTIFIER)
        self.text_editor.tag_configure("number", foreground=Theme.S_NUMBER)
        self.text_editor.tag_configure("definition", foreground=Theme.S_DEFINITION)
        self.text_editor.tag_configure("effect", foreground=Theme.S_EFFECT)
        self.text_editor.tag_configure("keyword", foreground=Theme.S_KEYWORD)
        self.text_editor.tag_configure("symbol", foreground=Theme.S_SYMBOL)

    def _get_tag_for_token(self, token): #converts token types from lexer into Tkinter tags
        match token.key:
            case TL.MEDIA:
                return "media"
            case TL.IDENTIFIER:
                return "identifier"
            case TL.NUMBER:
                return "number"
            case TL.DEFINITION:
                return "definition"
            case TL.EFFECT:
                return "effect"
            case TL.RENDER | TL.TIMELINE | TL.AFTER | TL.START_OF_VID | TL.END_OF_VID:
                return "keyword"
            case TL.ASSIGN | TL.UNION | TL.LPAREN | TL.RPAREN | TL.LBRACK | TL.RBRACK | TL.COMMA | TL.PERIOD | TL.COLON | TL.FUNC_COMP:
                return "symbol"
            case _:
                return None

    def highlight_syntax(self): #removes existing tags and applies new ones based on current text content and lexer tokens
        for tag in ["media", "identifier", "number", "definition", "effect", "keyword", "symbol"]:
            self.text_editor.tag_remove(tag, "1.0", "end")

        #Get content from editor and split into lines for processing
        content = self.text_editor.get("1.0", "end-1c")
        lines = content.split("\n")

        #process each line independently through lexer, splits line into tokens and 
        #applies syntax color based on token type and position in line
        for line_num, line in enumerate(lines, start=1):
            if not line.strip():
                continue
            try:
                tokens = self.lexer.build_tokens(line)
            except Exception as e:
                continue
            for token in tokens:
                if token.key == TL.END_OF_LINE:
                    continue
                tag_name = self._get_tag_for_token(token)
                if tag_name is None:
                    continue
                token_value = token.value
                if token_value == "":
                    continue
                
                #convert character positions into Tkinter text indices

                start_index = f"{line_num}.{token.start}"
                end_index = f"{line_num}.{token.end}"

                #apply syntax color to range corresponding to token
                self.text_editor.tag_add(tag_name, start_index, end_index)