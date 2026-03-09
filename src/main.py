from ui.Window import Window

def main():
    """
    Init UI class in here.
    """

    window = Window()
    window.CreateWindow()

    print("DVEL")


try:
    if __name__ == "__main__":
        main()
except NotImplementedError as ni:
    print(f'{ni}: unimplemented class.')
except Exception as e:
    print(e)

