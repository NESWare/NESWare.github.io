def add_subparser(subparsers):
    parser = subparsers.add_parser("serve", help="Serve the project")
    parser.add_argument("qwerty", help="Example argument for serve")


def run(args):
    print(f"Running serve with qwerty: {args.qwerty}")
