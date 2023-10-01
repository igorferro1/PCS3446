from .system import os


def main():
    print("Inicio")

    OS = os.OS()

    OS.boot()

    OS.run()


if __name__ == "__main__":
    main()
