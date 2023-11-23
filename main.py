import tkinter as tk
from gui import TenderApp

def main():
    root = tk.Tk()
    root.title("Rate Analysis")
    # root.geometry("3840x2160")
    root.attributes('-fullscreen', True)
    app = TenderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
