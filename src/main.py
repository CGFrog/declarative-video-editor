from ui.Window import Window


def main()->None:
    window = Window()
    window.run()

    """
    Creation of tkinter widgets would go here (make sure to import classes at the top)
    e.x. textEditor.CreateTextBox(window.left_frame)
         videoPlayer.ShowMediaViewer(window.right_frame)
    """

    window.root.mainloop()


try:
    if __name__ == "__main__":
        main()
except NotImplementedError as ni:
    print(f'{ni}: unimplemented class.')
except Exception as e:
    print(e)

