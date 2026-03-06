import subprocess
import sys
import os


class Application:

    @staticmethod
    def run_code(path: str) -> None:
        if os.path.exists(path):
            subprocess.run([sys.executable, path])
        else:
            raise FileNotFoundError(f"Invalid path {path} to .print file.")


def main() -> None:

    app = Application()

if __name__ == "__main__":
    main()