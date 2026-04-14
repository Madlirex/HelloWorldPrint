import subprocess
import sys

from scripts.transpiling.transpiler import Transpiler
from scripts.parsing.parser import Parser
from scripts.tokenizing.tokenizer import Tokenizer
from pathlib import Path

class Compiler:

    ENCODING = "utf-8"

    def __init__(self, tokenizer: Tokenizer, parser: Parser, transpiler: Transpiler) -> None:
        self.tokenizer = tokenizer
        self.parser = parser
        self.transpiler = transpiler

        self.src_root: Path = Path("")
        self.bin_root: Path = Path("")

    def compile(self, path: str) -> None:

        self.src_root = Path(path)
        self.src_root = self.src_root.resolve(False)
        self.src_root = self.src_root.with_suffix(".print")

        file = self.src_root.name

        self.src_root = self.src_root.parent

        self.bin_root = self.src_root / "bin"

        if not self.check_file(self.src_root / file):
            return

        self.compile_file(self.src_root / file)
        self.run_code((self.bin_root / file).with_suffix(".py"))

    def compile_file(self, path: Path) -> None:

        print(path)
        print(self.src_root)

        if not self.check_file(path):
            return

        with path.open("r", encoding=Compiler.ENCODING) as f:
            data: str = f.read()

        tokens = self.tokenizer.tokenize(data)
        ast = self.parser.parse_program(tokens)
        compiled_code, files = self.transpiler.transpile_program(ast)

        path = self.get_bin_path(path).with_suffix(".py")
        self.ensure_dir(path.parent)

        with path.open("w", encoding=Compiler.ENCODING) as f:
            f.write(compiled_code)

        for file in files:
            p = self.src_root / Path(*file.split(".")).with_suffix(".print")
            self.compile_file(p)

    def check_file(self, path: Path) -> bool:
        if not path.exists():
            print(f"Invalid path {path} to file.")
            return False
        return True

    def convert_str_to_path(self, *path: str) -> Path:
        p = Path(*path)
        p = p.resolve(False)

        return p

    def get_bin_path(self, path: Path) -> Path:
        return self.bin_root / path.relative_to(self.src_root)

    def ensure_dir(self, path: Path) -> None:
        if path.exists() and not path.is_dir():
            raise ValueError(f"{path} exists and is not a directory")
        path.mkdir(parents=True, exist_ok=True)

    def run_code(self, path: Path) -> None:
        path = path.with_suffix(".py")

        if not self.check_file(path):
            return

        print("----------------------- RESULT -----------------------")
        print(path)

        if getattr(sys, 'frozen', False):
            # Running inside PyInstaller
            subprocess.run(["python", str(path)])
        else:
            subprocess.run([sys.executable, str(path)])

        print("RAN")


def compile_print(path: str) -> None:
    tokenizer = Tokenizer()
    parser = Parser()
    transpiler = Transpiler()
    compiler = Compiler(tokenizer, parser, transpiler)
    compiler.compile(path)

def main() -> None:
    compile_print(input("Enter path to .print file: "))

if __name__ == '__main__':
    main()
