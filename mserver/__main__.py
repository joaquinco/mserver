import sys
from argparse import ArgumentParser

import mserver


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('action', choices=['listen_mpd', 'run_server'])

    return parser.parse_args(sys.argv[1:])


def main():
    args = parse_args()

    getattr(mserver, args.action)()


if __name__ == '__main__':
    main()
