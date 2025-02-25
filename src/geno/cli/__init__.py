import argparse
import importlib


def main():
    parser = argparse.ArgumentParser(description="My CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    commands = ["new", "build", "serve", "version"]
    for command in commands:
        module = importlib.import_module(f"geno.cli.commands.{command}")
        module.add_subparser(subparsers)

    args = parser.parse_args()

    if args.command:
        module = importlib.import_module(f"geno.cli.commands.{args.command}")
        module.run(args)
    else:
        parser.print_help()
