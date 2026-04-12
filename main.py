import click

from scripts.compiler import compile_print

@click.command()
@click.argument("path")
def cli(path: str):
    compile_print(path)


if __name__ == "__main__":
    cli()