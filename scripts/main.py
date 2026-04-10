from scripts.transpiling.transpiler import Transpiler
from scripts.parsing.parser import Parser
from scripts.tokenizing.tokenizer import Tokenizer
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
    def compile_code(path: str, root: str = None) -> None:
        if not path:
            return

        if not os.path.exists(path):
            return

        with open(path, encoding=Compiler.ENCODING) as f:
            code = f.read()
            tokenizer = Tokenizer(code)
            tokens = tokenizer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse_program()
            trans = Transpiler(ast)
            compiled_code, modules = trans.transpile_program()

        name = Compiler.get_basename(path) + ".py"
        root = Compiler.get_directory(path) if not root else root
        files = Compiler.convert_modules_to_paths(modules)
        for f in files:
            Compiler.compile_code(root + f + ".print", root)

        folder = Compiler.get_bin_directory(path, root)
        Compiler.create_dir(folder)
        Compiler.create_file(folder + name)
        with open(folder + name, 'w', encoding=Compiler.ENCODING) as f:
            f.write(compiled_code)

    @staticmethod
    def convert_modules_to_paths(modules: list[str]) -> list[str]:
        return [Compiler.convert_module_to_path(module) for module in modules]

    @staticmethod
    def convert_module_to_path(module: str) -> str:
        return module.replace(".", "/")

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
    def get_bin_directory(path: str, root: str) -> str:
        return root + "bin/" + Compiler.get_directory(path).removeprefix(root)

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
    file = input("Path to root .print file: ")
    Compiler.load_file(file)
    Compiler.run_code(Compiler.get_directory(file) + "bin/" + Compiler.get_basename(file) + ".py")

if __name__ == "__main__":
    main()