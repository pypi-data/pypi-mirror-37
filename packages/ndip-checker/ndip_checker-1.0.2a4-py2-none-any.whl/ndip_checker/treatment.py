# encoding: utf-8
import os
import copy
import json
import codecs

from datetime import datetime, timedelta

from items import ITEMS, check, command_confirm
from patient import update_patient_enter_date

KEY_TREAT_LIST = 'treatlist'
KEY_CHECKS = 'form'
KEY_TAG_DATE = 'tagDate'
KEY_IS_STARTED = 'is_started'
KEY_EXPECT_DATE = 'expectdate'
KEY_ACTUAL_DATE = 'actualdate'

VALUE_DYNAMIC_ADD = u'动态增加'

DATE_FORMAT = '%Y-%m-%d'


class Treat:
    """Represents a patient's one treatment record."""

    def __init__(self, json_obj, patient_name='', fix=False):
        self.data = json_obj
        self.patient_name = patient_name
        self.expected = self.data[KEY_EXPECT_DATE]
        self.fix = fix

    def check(self):
        """return value is whether treatment has did at least once fix."""

        # Only check Dynamic added treatment.
        try:
            if self.data[KEY_TAG_DATE] != VALUE_DYNAMIC_ADD:
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

    def update_enter_date(self, enter_date):
        """update enter date to target enter date.

        return value is whether this Treat has been modified.
        """

        # skip update dynamic added treatments
        if self.data[KEY_TAG_DATE] == VALUE_DYNAMIC_ADD:
            print('动态病程，无需调整。')
            return False

        # get target date
        stage = int(self.data['stage'].split()[0])
        origin = datetime.strptime(enter_date, DATE_FORMAT)
        target = origin + timedelta(weeks=stage)
        target_date = datetime.strftime(target, DATE_FORMAT)

        prompt = "update treatment date from '{}' to '{}'? [Y/n]".format(self.expected, target_date)
        if not command_confirm(prompt):
            print("You've cancelled this update.")
            return False

        # if not started, change actual date
        if not self.data.get(KEY_IS_STARTED, False):
            origin = self.data[KEY_ACTUAL_DATE]
            print("treatment not started, update actual date from '{}' to '{}'".format(origin, target_date))
            self.data[KEY_ACTUAL_DATE] = target_date

        # update expect date
        origin = self.data[KEY_EXPECT_DATE]
        print("update expect date from '{}' to '{}'".format(origin, target_date))
        self.data[KEY_EXPECT_DATE] = target_date

        # update tag date as: stage + ' ' + expected date
        origin = self.data[KEY_TAG_DATE]
        tag_date = self.data['stage'] + ' ' + target_date
        print(u"update tag date from '{}' to '{}'".format(origin, tag_date))
        self.data[KEY_TAG_DATE] = tag_date

        return True


class Treatment:
    """Represents a patient's all treatment record."""

    # TODO: refactor fix to check method
    # TODO: encapsulate patient info to a object
    def __init__(self, json_obj, record_id, patient_id, patient_name=None, fix=False):
        """init treatment."""

        self.record_id = record_id
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.data = json_obj
        self.fix = fix

        self._backup_data = copy.deepcopy(json_obj)  # for backup record

    def _backup(self):
        """Back up data.

        1. backup path is `~/.ndip_checker`
        2. backup file name format: `<record-id> - timestamp.json`
        """

        user_home = os.environ['HOME']
        path = os.path.join(user_home, 'ndip_checker')
        if not os.path.exists(path):
            os.makedirs(path)

        timestamp = str(datetime.now())
        name = "{} - {}.json".format(self.record_id, timestamp)

        filename = os.path.join(path, name)
        with codecs.open(filename, 'w', 'utf-8') as fp:
            json.dump(self._backup_data, fp, ensure_ascii=False, indent=4)

    def check(self, db):
        fixed = False
        for data in self.data[KEY_TREAT_LIST]:
            treat = Treat(data, self.patient_name, self.fix)
            if treat.check():
                fixed = True

        if self.fix and fixed:
            self.update(db)

        return fixed

    def update(self, db):
        """Update the treatment record to database."""

        prompt = "Do you really want to update patient's changes to DB? [Y/n]"
        if not command_confirm(prompt):
            return False

        # backup original data to file
        self._backup()

        # commit changes to DB
        data = json.dumps(self.data, ensure_ascii=False)
        sql = "UPDATE hospital_record set treatment=%s where id=%s"
        val = (data, self.record_id)

        cur = db.cursor()
        cur.execute(sql, val)

        db.commit()
        print(cur.rowcount, " record(s) affected in hospital_record")

        return True

    @property
    def enter_date(self):
        """return patient's enter_date."""
        # TODO: need to valid enter_date from hospital_patient too

        return self.data[KEY_TREAT_LIST][0][KEY_EXPECT_DATE]

    def update_enter_date(self, target, patient_id, db):
        """update patient's enter date"""

        # confirm format as YYYY-MM-DD, as format like `2018-3-14` is accepted

        # update each treat
        changed = False
        for data in self.data[KEY_TREAT_LIST]:
            treat = Treat(data)
            if treat.update_enter_date(target):
                changed = True

        # update treatment, besides patient's info also need to update.
        if changed:
            if self.update(db):
                update_patient_enter_date(patient_id, db, target)
