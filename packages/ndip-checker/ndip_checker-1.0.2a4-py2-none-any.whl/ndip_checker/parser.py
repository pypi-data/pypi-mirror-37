# encoding: utf-8
import argparse


def get_parser():
    """get command parser."""
    parser = argparse.ArgumentParser(
        description="check and fix errors in NDIP",
        epilog="""
        check/fix 涂片/培养/病程记录
        """
    )
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
    parser.add_argument("-f", "--fix",
                        action="store_true",
                        help="whether fix error, default False.")
    return parser

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    print(args.host)
    print(args.user)
    print(args.password)
    print(args.database)
    print(args.fix)


