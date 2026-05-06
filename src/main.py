from ui.Window import Window


def main()->None:
    window = Window()
    window.run()

try:
    if __name__ == "__main__":
        main()
except NotImplementedError as ni:
    print(f'{ni}: unimplemented class.')
except Exception as e:
    print(e)

