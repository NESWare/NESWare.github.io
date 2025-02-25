from geno import __version__


def add_subparser(subparsers):
    parser = subparsers.add_parser("version", help="Show version information")


def run(args):
    print(f"geno {__version__}")
