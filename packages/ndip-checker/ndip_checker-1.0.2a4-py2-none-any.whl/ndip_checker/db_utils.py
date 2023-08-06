# encoding: utf-8
import json
import MySQLdb


def get_db(args):
    """return a db object based on parameters in args."""

    return MySQLdb.connect(
        host=args.host, db=args.database,
        user=args.user, passwd=args.password,
        charset='utf8')


def get_all_objects(args):
    pass
