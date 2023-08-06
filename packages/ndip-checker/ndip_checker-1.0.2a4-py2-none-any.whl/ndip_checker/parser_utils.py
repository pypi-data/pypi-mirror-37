# encoding: utf-8
import argparse

from datetime import datetime

from handler import handler_check_dynamic_treats, handler_change_enter_date, handle_check_all

DATE_FORMAT = '%Y-%m-%d'


def valid_date(s):
    try:
        t = datetime.strptime(s, DATE_FORMAT)
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

    return datetime.strftime(t, DATE_FORMAT)


def get_parser():
    """get command parser."""
    parser = argparse.ArgumentParser(
        description="check and fix errors in NDIP", )
    parser.add_argument("-o", "--host",
                        default="localhost",
                        help="mysql host, default localhost")
    parser.add_argument("-u", "--user",
                        default="root",
                        help="mysql user, default root")
    parser.add_argument("-p", "--password",
                        default="ChangeMe1!",
                        help="mysql password, default ChangeMe1!")
    parser.add_argument("-d", "--database",
                        default="hospitalAdmin",
                        help="mysql database, default hospitalAdmin")

    subparsers = parser.add_subparsers(help='operations')

    # check all treatments
    check_all_parser = subparsers.add_parser('all', help='check all treatments')
    check_all_parser.set_defaults(func=handle_check_all)

    # check dynamic treatments
    dynamic_treat_parser = subparsers.add_parser(
        'dynamic-treat', help='check dynamic treatments')
    dynamic_treat_parser.add_argument(
        '-f', '--fix', action='store_true',
        help='fix error founded in dynamic treatments')
    dynamic_treat_parser.set_defaults(func=handler_check_dynamic_treats)

    # change enter date
    change_enter_date_parser = subparsers.add_parser(
        'change-enter-date', help="change patient's enter date")
    change_enter_date_parser.add_argument(
        'record_id', action='store', type=int,
        help='patient treatment record ID')
    change_enter_date_parser.add_argument(
        'original', action='store', type=valid_date,
        help='original enter date - format YYYY-MM-DD')
    change_enter_date_parser.add_argument(
        'target', action='store', type=valid_date,
        help='target enter date - format YYYY-MM-DD')
    change_enter_date_parser.set_defaults(func=handler_change_enter_date)

    return parser


def parse_args(args):
    """return parsed args"""

    parser = get_parser()
    return parser.parse_args(args)
