import builtins

RENAMES = {
    "vytlač": "print",
    "vtlač": "input",
    "dĺžka": "len",
    "rozsah": "range"
}

def _make_blocked(old_name, new_name):
    def blocked(*args, **kwargs):
        raise RuntimeError(f"Use '{new_name}' instead of '{old_name}'")
    return blocked

for new_name, old_name in RENAMES.items():
    original = getattr(builtins, old_name)

    globals()[new_name] = original

    globals()[old_name] = _make_blocked(old_name, new_name)

import tkinter as tk
class Application():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.geometry("600x600")
        self.buttons = []
        for i in rozsah(3):
            self.buttons.append([])
            for j in rozsah(3):
                self.buttons[i].append(tk.Button(self.root))
                self.buttons[i][j].grid(row = i, column = j)
            else:
                pass

        else:
            pass

        self.update()

    def update(self):
        self.root.mainloop()


if __name__ == "__main__":
    Application()
else:
    pass

