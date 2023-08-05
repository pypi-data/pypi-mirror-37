# encoding: utf-8


def update_patient_enter_date(patient_id, db, enter_date):
    """update patient's information."""

    sql = "UPDATE hospital_patient set enter_date=%s where id=%s"
    val = (enter_date, patient_id)

    cur = db.cursor()
    cur.execute(sql, val)

    db.commit()
    print(cur.rowcount, " record(s) affected in hospital_patient")

    return True
