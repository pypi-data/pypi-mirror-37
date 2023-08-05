# encoding: utf-8
import json
import MySQLdb

from parser import get_parser
from treatment import Treatment

parser = get_parser()
args = parser.parse_args()

host = args.host
user = args.user
password = args.password
db_name = args.database
fix = args.fix
db = MySQLdb.connect(host=host, user=user, passwd=password, db=db_name, charset='utf8')

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

    treatment = Treatment(record_id, patient_id, patient_name, data, fix)
    treatment.check(db)

db.close()
