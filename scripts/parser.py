class Parser:

    @staticmethod
    def parse_code(code: str) -> tuple[str, list[str]]:
        pass

if __name__ == "__main__":
    with open("parser_test.print", "r", encoding="utf-8") as f:
        print(Parser.parse_code(f.read())[0])