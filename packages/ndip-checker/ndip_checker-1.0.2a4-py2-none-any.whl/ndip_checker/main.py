# encoding: utf-8
import sys

from parser_utils import parse_args


def execute_from_command_line():
    """run script"""

    args = parse_args(sys.argv[1:])
    args.func(args)

if __name__ == "__main__":
    execute_from_command_line()
