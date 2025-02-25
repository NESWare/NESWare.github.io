import pathlib

import geno.generator


def add_subparser(subparsers):
    parser = subparsers.add_parser("build", help="Build the project")
    parser.add_argument(
        "configuration", type=pathlib.Path, help="geno configuration file"
    )


def run(args):
    geno.generator.run(args.configuration)
