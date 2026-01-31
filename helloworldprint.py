import os


def decode_to_command(text: str) -> tuple[str, str]:
    start = text.index('(') + 1
    end = text.index(')')
    if text[start] == '"' or (text[start + 1] == '"' and text[start] == "f"):
        start += 1 if text[start] != "f" else 2
        end -= 1
        arg = f"\"{text[:start - (2 if text[start-2] != "f" else 3):]}\""
        if text[start-2] == "f":
            arg = "f" + arg
    else:
        arg = f"{text[:start - 1:]}"
    command = text[start:end]

    return command, arg

def execute_command(command: str, arg: str) -> object:
    try:
        return eval(f"{command}({arg})", globals())
    except SyntaxError:
        exec(f"{command}({arg})", globals())


path = input("Path to a .print file (relative/absolute): ")
while not (os.path.exists(path) and path.endswith(".print")):
    print(f"Invalid path: {path}")
    path = input("Path to a .print file (relative/absolute): ")

raw_text: str
with open(path, "r") as file:
    raw_text = file.read()

for line in raw_text.split("\n"):
    execute_command(*decode_to_command(line))
