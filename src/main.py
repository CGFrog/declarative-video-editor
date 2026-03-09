def main():
    """
    Init UI class in here.
    """
    print("DVET")


try:
    if __name__ == "__main__":
        main()
except NotImplementedError as ni:
    print(f'{ni}: unimplemented class.')
except Exception as e:
    print(e)

