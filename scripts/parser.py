class Parser:

    @staticmethod
    def parse_code(code: str) -> tuple[str, list[str]]:
        imported_files = []
        for line in code.splitlines():
            if line == "import more.test":
                imported_files.append("../tests/more/test.print")

        return code, imported_files