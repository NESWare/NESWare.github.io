def add_subparser(subparsers):
    parser = subparsers.add_parser("new", help="Initialize a project")
    parser.add_argument("qwerty", help="Example argument for new")


def run(args):
    print(f"Running new with qwerty: {args.qwerty}")
