import tkinter as tk

class Window:
    def __init__(self):
        pass

    def CreateWindow(self):
        root = tk.Tk()

        root.title("Declarative Video Editor")
        root.geometry("400x300")

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        main_frame = tk.Frame(root, bg ="YELLOW")
        main_frame.grid(row=0, column=0, sticky="nsew")

        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        left_frame = tk.Frame(main_frame, bg ="BLUE")
        left_frame.grid(row=0, rowspan=2, column=0, sticky="nsew")

        right_frame = tk.Frame(main_frame, bg ="GREEN")
        right_frame.grid(row=0, column=1, sticky="nsew")

        bottom_frame = (
        tk.Frame(main_frame, bg = "RED"))
        bottom_frame.grid(row=1, column=1, sticky="nsew")

        root.mainloop()