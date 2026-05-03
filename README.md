# PRINT Programming Language

PRINT is a dynamically typed programming language based off of Python. Its development started in early 2026 by [@Madlirex](https://www.github.com/madlirex) and was finished by April 2026.  
It is as fast as Python since it compiles directly to it, but more of that can be seen in the [architecture](ARCHITECTURE.md) explanation.

The language of course has its own rules which can be found in the [rules file](RULES.md).

## How To Run

There are 3 ways how to run a .print file:

### Executable

Add the [printpp.exe](dist/printpp.exe) file to your PATH (environment variables) or run it through absolute path (e.g. `C:/User/Downloads/HelloWorld/dist/printpp.exe`)  and provide 1 argument, which is either absolute or relative path to your root PRINT file. Example:
`printpp main.print`

### Python Interpreter

Alternatively, you can use the Python interpreter to either run the [main.py](main.py) file or [compiler.py](scripts/compiler.py) file.  
Only difference between these two is, that [compiler.py](scripts/compiler.py) doesn't take any arguments, instead it asks for your root PRINT file in a console dialog, while [main.py](main.py) requires you to put the path as an argument, either absolute or relative. Example: `python main.py tests/helloworld`
