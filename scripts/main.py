import subprocess
import sys


class Application:

    @staticmethod
    def run_code(path: str) -> None:
        with open(path, 'r') as f:
            subprocess.run([sys.executable, path])

def main() -> None:

    app = Application()

if __name__ == "__main__":
    main()