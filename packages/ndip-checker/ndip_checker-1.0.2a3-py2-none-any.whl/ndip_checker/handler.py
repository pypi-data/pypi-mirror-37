# encoding: utf-8
import json
import MySQLdb

from treatment import Treatment


def get_db(args):
    """get db handler"""

    return MySQLdb.connect(
        host=args.host, db=args.database,
        user=args.user, passwd=args.password,
        charset='utf8')


def handle_check_all(args):
    """check all treatment stictly"""

    print("Not support yet.")


def handler_check_dynamic_treats(args):
    """check dynamic arguments."""
    db = get_db(args)

    cur = db.cursor()
    cur.execute("select id, treatment, patient_id from hospital_record")

    for row in cur.fetchall():
        record_id = row[0]
        data = json.loads(row[1])
        patient_id = row[2]
        cur2 = db.cursor()
        sql = "select code from hospital_patient where id={}".format(patient_id)
        cur2.execute(sql)
        patient_name = cur2.fetchall()[0][0]

        treatment = Treatment(data, record_id, patient_id, patient_name, args.fix)
        treatment.check(db)

    db.close()


def handler_change_enter_date(args):
    """change patient's enter date."""

    db = get_db(args)
    cur = db.cursor()

    # get treatment record
    sql = "SELECT treatment, patient_id FROM hospital_record WHERE id={}".format(args.record_id)
    print(sql)
    cur.execute(sql)
    record = cur.fetchone()
    data = json.loads(record[0])
    patient_id = int(record[1])

    treatment = Treatment(data, args.record_id, patient_id)

    # if enter date not equals to the given `original parameter, quit
    if treatment.enter_date != args.original:
        msg = "original enter date {} not match existing: {}".format(args.original, treatment.enter_date)
        print(msg)

        return False

    treatment.update_enter_date(args.target, patient_id, db)

    db.close()
