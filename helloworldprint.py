import os


def decode_to_command(text: str) -> tuple[str, str]:
    start = len(text) - text[::-1].index('(')
    end = len(text) - text[::-1].index(')') - 1
    if text[start] == '"' or (text[start + 1] == '"' and text[start] == "f"):
        start += 1 if text[start] != "f" else 2
        end -= 1
        arg = f"\"{text[:start - (2 if text[start - 2] != "f" else 3):]}\""
        if text[start - 2] == "f":
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


def expand_path(x: str) -> str:
    if not x.endswith('.print'):
        return x + '.print'
    elif not os.path.exists(x):
        return x + '.print'
    return x


path = input("Path to a .print file (relative/absolute): ")
path = expand_path(path)
while not os.path.exists(path):
    print(f"Invalid path: {path}")
    path = input("Path to a .print file (relative/absolute): ")
    path = expand_path(path)

raw_text: str
with open(path, "r") as file:
    raw_text = file.read()

ignored = False

for line in raw_text.split("\n"):
    if line.isspace() or line == "" or line[0] == "#":
        continue
    if not ignored and line[0:3] == '"""':
        ignored = True
        continue
    if ignored and line.endswith('"""'):
        ignored = False
        continue
    if ignored:
        continue
    execute_command(*decode_to_command(line))
