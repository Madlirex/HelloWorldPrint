import locale
from Lib.test.test_decimal import directory

from parser import Parser
import subprocess
import sys
import os


class Compiler:

    ENCODING = "utf-8"

    @staticmethod
    def load_file(path: str) -> None:
        file = Compiler.file_with_extension_exists(path, "print")
        if file:
            Compiler.compile_code(file)
        else:
            Compiler.print_invalid_path(path, "print")

    @staticmethod
    def compile_code(path: str) -> None:
        with open(path, encoding=Compiler.ENCODING) as f:
            code = f.read()
            parsed_code = Parser.parse_code(code)
        name = Compiler.get_basename(path) + ".py"
        folder = Compiler.get_directory(path) + "bin/"
        Compiler.create_dir(folder)
        Compiler.create_file(folder + name)
        with open(folder + name, 'w', encoding=Compiler.ENCODING) as f:
            f.write(code)

    @staticmethod
    def create_file(path: str) -> None:
        if not os.path.exists(path):
            open(path, 'x', encoding=Compiler.ENCODING).close()

    @staticmethod
    def create_dir(path: str) -> None:
        if not os.path.exists(path):
            os.mkdir(path)

    @staticmethod
    def get_basename(path: str) -> str:
        name = os.path.basename(path)
        return os.path.splitext(name)[0]

    @staticmethod
    def get_directory(path: str) -> str:
        return path.removesuffix(os.path.basename(path))

    @staticmethod
    def file_with_extension_exists(path: str, extension: str) -> str | None:
        extension = Compiler.format_extension(extension)
        if not path.endswith(extension):
            path += extension
        return path if os.path.exists(path) else None

    @staticmethod
    def format_extension(extension: str) -> str:
        return extension if extension.startswith(".") else f".{extension}"

    @staticmethod
    def print_invalid_path(path: str, extension: str) -> None:
        extension = Compiler.format_extension(extension)
        print(f"Invalid path {path} to {extension} file.")

    @staticmethod
    def run_code(path: str) -> None:
        file = Compiler.file_with_extension_exists(path, "py")
        if file:
            subprocess.run([sys.executable, file])
        else:
            Compiler.print_invalid_path(path, "py")


def main() -> None:
    Compiler.load_file(input("Path to root .print file: "))

if __name__ == "__main__":
    main()