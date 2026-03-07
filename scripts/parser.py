class Parser:

    keywords = {
        "čo ak": "if",
        "ibaže": "elif",
        "inak": "else",
        "kým platí, že": "while",
        "pre každé": "for",
        "trieda": "class",
        "definuje": "def",
        "skús": "try",
        "okrem": "except",
        "na koniec": "finally",
        "in": "v",
        "sa rovná": "==",
        "je menšie ako": "<",
        "je väčšie ako": ">",
        "je menšie alebo rovné ako": "<=",
        "je väčšie alebo rovné ako": ">=",
        "sa nerovná": "!=",
        "neplatí": "not",
        "alebo": "or",
        "a": "and",
        "je": "is",
        "definuj": "def",
        "zmaž": "del",
        "vráť": "return",
        "výnos": "yield",
        "ako": "as",
        "importuj": "import",
        "z": "from",
        "zlom": "break",
        "pokračuj": "pass",
        "preskoč": "continue",
        "klamstvo": "False",
        "pravda": "True",
        "nič": "None",
        "verejné": "global",
        "nelokálna": "nonlocal",
        "využi": "with",
        "porovnaj": "match",
        "v prípade, že": "case",
        "vyvráť": "raise",
        "skrátená funkcia, väčšinou anonymná a bez mena, používa sa pri krátkych operáciach alebo vo vnútri funkcií ako argument": "lambda"
    }

    is_string = False
    string_mode = ""
    is_comment = False
    multiline_comment = 0

    @staticmethod
    def parse_code(code: str) -> tuple[str, list[str]]:
        imported_files = []
        code = Parser.parse_lines(code)
        max_indent = Parser.get_biggest_indent(code)
        code = Parser.indent_code(code, max_indent)

        return code, imported_files

    @staticmethod
    def get_biggest_indent(code: str) -> int:
        indent = 0
        for line in code.splitlines():
            curr_indent = Parser.get_indent(line)
            indent = curr_indent if curr_indent > indent else indent

        return indent

    @staticmethod
    def get_indent(line: str) -> int:
        return len(line) - len(line.lstrip(" "))

    @staticmethod
    def indent_code(code: str, indent: int) -> str:
        result = ""
        for line in code.splitlines():
            to_indent = indent - Parser.get_indent(line)
            result += " " * to_indent + line.lstrip(" ") + "\n"
        return result

    @staticmethod
    def parse_lines(code: str) -> str:
        result = ""
        for line in code.splitlines():
            result += Parser.parse_line(line) + "\n"
        return result

    @staticmethod
    def parse_line(line: str) -> str:
        indent = Parser.get_indent(line)
        line = line.lstrip(" ")

        Parser.is_string = False
        Parser.is_comment = Parser.multiline_comment == 3
        Parser.string_mode = ""

        for char in line:
            Parser.evaluate_string(char)

        return " " * indent + line

    @staticmethod
    def evaluate_string(char: str) -> None:
        if char == "\"" or char == "'" and not (Parser.is_string or Parser.is_comment):
            Parser.is_string = True
            Parser.string_mode = char
        elif char == Parser.string_mode and Parser.is_string:
            Parser.is_string = False
            Parser.string_mode = ""

    @staticmethod
    def evaluate_comment(char: str) -> None:
        if char == "#" and not Parser.is_string:
            Parser.is_comment = True
        elif char == "\"":
            Parser.multiline_comment += 1
        if Parser.multiline_comment == 3:
            Parser.is_comment = True
            Parser.is_string = False
        elif Parser.multiline_comment > 3:
            Parser.multiline_comment -= Parser.multiline_comment - 3

    @staticmethod
    def parse_keywords(line: str) -> str:
        for key in Parser.keywords:
            if line.startswith(key):
                return Parser.keywords[key] + line.removeprefix(key)
        return line

    @staticmethod
    def parse_expression(func: str, arg: str) -> str:
        if func.startswith("f\""):
            result = f"{func[2:-1]}(f\"{arg}\")"
        elif func.startswith("\""):
            result = f"{func[1:-1]}(\"{arg}\")"
        else:
            result = f"{func}({arg})"
        return result

if __name__ == "__main__":
    with open("parser_test.print", "r", encoding="utf-8") as f:
        print(Parser.parse_code(f.read())[0])