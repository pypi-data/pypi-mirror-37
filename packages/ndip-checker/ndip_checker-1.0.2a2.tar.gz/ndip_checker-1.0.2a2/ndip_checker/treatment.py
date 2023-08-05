# encoding: utf-8
import json

from items import ITEMS, check, command_confirm


KEY_TREATLIST = 'treatlist'
KEY_EXPECT_DATE = 'expectdate'
KEY_CHECKS = 'form'
KEY_TAG = 'tagDate'
VALUE_DYNAMIC_ADD = u'动态增加'


class Treat:
    """Represents a patient's one treatment record."""

    def __init__(self, json_obj, patient_name, fix):
        self.data = json_obj
        self.patient_name = patient_name
        self.expected = self.data[KEY_EXPECT_DATE]
        self.fix = fix

    def check(self):
        """return value is whether treatment has did at least once fix."""

        # Only check Dynamic added treatment.
        try:
            if self.data[KEY_TAG] != VALUE_DYNAMIC_ADD:
                return False
        except KeyError:
            # skip the treatment if tagDate not exist
            print(u"{} 于 {} 填写的病程 tagDate 为空，请检查！".format(self.patient_name, self.expected))
            return False

        fixed = False
        for item in self.data[KEY_CHECKS]:
            if item['item'] in ITEMS.keys():
                if check(item, self.patient_name, self.expected, self.fix):
                    fixed = True

        if self.fix and fixed:
            self.update()

        return fixed

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
        fixed = False
        for data in self.data[KEY_TREATLIST]:
            treat = Treat(data, self.patient_name, self.fix)
            if treat.check():
                fixed = True

        prompt = "Do you really want to update {}'s changes to DB? [Y/n]".format(self.patient_name)
        if self.fix and fixed and command_confirm(prompt):
            self.update(db)

        return fixed

    def update(self, db):
        """Update the treatment record to database."""
        data = json.dumps(self.data, ensure_ascii=False)
        sql = "UPDATE hospital_record set treatment=%s where id=%s"
        val = (data, self.record_id)

        cur = db.cursor()
        cur.execute(sql, val)

        db.commit()
        print(cur.rowcount, " record(s) affected")
