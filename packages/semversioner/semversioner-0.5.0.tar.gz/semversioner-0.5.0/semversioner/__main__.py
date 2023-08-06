import sys

from .cli import cli

def main(args=None):
    """The main routine."""
    cli(obj={})

if __name__ == '__main__':
    sys.exit(main())