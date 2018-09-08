import sys
from argparse import ArgumentParser

import mserver

_commands_args = {
    'run_server': [
        (['--host'], {}),
        (['-p', '--port'], {}),
    ],
    'listen_mpd': []
}


def parse_args(args):
    parser = ArgumentParser()
    parser.add_argument('action', choices=_commands_args.keys())

    return parser.parse_known_args(args)


def _parse_command_args(cmd_name, cmd_args):
    parser_entries = _commands_args.get(cmd_name)

    if not parser_entries:
        return {}

    parser = ArgumentParser()

    for args, kwargs in parser_entries:
        parser.add_argument(*args, **kwargs)

    return vars(parser.parse_args(cmd_args))


def main():
    args, extra = parse_args(sys.argv[1:])

    getattr(mserver, args.action)(**_parse_command_args(args.action, extra))


if __name__ == '__main__':
    main()
