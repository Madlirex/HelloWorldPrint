class Parser:

    @staticmethod
    def parse_code(code: str) -> tuple[str, list[str]]:
        imported_files = []
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

if __name__ == "__main__":
    with open("parser_test.print", "r") as f:
        print(Parser.parse_code(f.read()))