# encoding: utf-8
import json

from items import ITEMS, check


KEY_TREATLIST = 'treatlist'
KEY_EXPECT_DATE = 'expectdate'
KEY_CHECKS = 'form'


class Treat:
    """Represents a patient's one treatment record."""

    def __init__(self, json_obj, patient_name, fix):
        self.data = json_obj
        self.patient_name = patient_name
        self.expected = self.data[KEY_EXPECT_DATE]
        self.fix = fix

    def check(self):
        valid = True
        for item in self.data[KEY_CHECKS]:
            if item['item'] in ITEMS.keys():
                if not check(item, self.patient_name, self.expected, self.fix):
                    valid = False

        if self.fix and not valid:
            self.update()

        return valid

    def update(self):
        """update treatment status from `complete` to `im-progress`"""
        self.data['classType'] = 'in-progress'
        self.data['fix-info'] = 'fix by NDIP checker.'


class Treatment:
    """Represents a patient's all treatment record."""

    def __init__(self, record_id, patient_id, patient_name, json_obj, fix=False):
        """init treatment."""
        self.record_id = record_id
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.data = json_obj
        self.fix = fix

    def check(self, db):
        valid = True
        for data in self.data[KEY_TREATLIST]:
            treat = Treat(data, self.patient_name, self.fix)
            if not treat.check():
                valid = False

        if self.fix and not valid:
            self.update(db)

        return valid

    def update(self, db):
        """Update the treatment record to database."""
        data = json.dumps(self.data)
        sql = "UPDATE hospital_record set treatment=%s where id=%s"
        val = (data, self.record_id)

        cur = db.cursor()
        cur.execute(sql, val)

        db.commit()
        print(cur.rowcount, " record(s) affected")
