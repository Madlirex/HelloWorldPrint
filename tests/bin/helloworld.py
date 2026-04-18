import tkinter as tk
class Application():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.geometry("600x600")
        self.update()

    def update(self):
        self.root.mainloop()


if __name__ == "__main__":
    Application()
else:
    pass

