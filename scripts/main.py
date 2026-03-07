import subprocess
import sys
import os


class Compiler:

    @staticmethod
    def file_with_extension_exists(path: str, extension: str) -> str | None:
        extension = extension if extension.startswith(".") else f".{extension}"
        if not path.endswith(extension):
            path += extension
        return path if os.path.exists(path) else None


    @staticmethod
    def run_code(path: str) -> None:
        file = Compiler.file_with_extension_exists(path, "py")
        if file:
            subprocess.run([sys.executable, file])
        else:
            raise FileNotFoundError(f"Invalid path {path} to .py file.")


def main() -> None:

    app = Compiler()

if __name__ == "__main__":
    main()