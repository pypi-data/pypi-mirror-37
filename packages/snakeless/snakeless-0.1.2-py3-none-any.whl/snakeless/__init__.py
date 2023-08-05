import sys

from .cli_controller import SnakelessCli


def main(argv=sys.argv[1:]):
    snakeless_cli = SnakelessCli()
    return snakeless_cli.run(argv)
