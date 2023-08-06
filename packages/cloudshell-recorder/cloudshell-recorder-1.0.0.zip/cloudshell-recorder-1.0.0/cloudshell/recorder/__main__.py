"""bootstrap.cli: executed when bootstrap directory is called as script."""
from cloudshell.recorder.bootstrap import cli


def init():
    cli()


if __name__ == "__main__":
    init()
