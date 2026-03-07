import subprocess
import sys
import os


class Compiler:

    @staticmethod
    def load_file(path: str) -> None:
        file = Compiler.file_with_extension_exists(path, "print")
        if file:
            with open(file, 'r') as f:
                code = file.read()
        else:
            Compiler.print_invalid_path(path, "print")

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