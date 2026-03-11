import tkinter as tk

class Window:
    def __init__(self):
        self.root = tk.Tk()
        pass

    def createWindow(self):
        self.root.title("Declarative Video Editor")
        self.root.geometry("400x300")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

    def createWindowLayout(self):
        self.main_frame = tk.Frame(self.root, bg="YELLOW")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

    def textEditorView(self):
        left_frame = tk.Frame(self.main_frame, bg="BLUE")
        left_frame.grid(row=0, rowspan=2, column=0, sticky="nsew")

    def videoDisplayView(self):
        right_frame = tk.Frame(self.main_frame, bg="GREEN")
        right_frame.grid(row=0, column=1, sticky="nsew")

    def consoleView(self):
        bottom_frame = tk.Frame(self.main_frame, bg="RED")
        bottom_frame.grid(row=1, column=1, sticky="nsew")

    def run(self):
        self.createWindow()
        self.createWindowLayout()
        self.textEditorView()
        self.videoDisplayView()
        self.consoleView()
        self.root.mainloop()