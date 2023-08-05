# encoding: utf-8
import uuid

from . import BaseItem, KEY_FIX_INFO, KEY_ID, KEY_FINISH_TAG, KEY_CLASS_STATUS


class BingChengJiLuItem(BaseItem):
    """培养检查项 """

    def __init__(self, json_obj, patient_name, expected_date):
        self.json_obj = json_obj
        self.data = json_obj['data']
        self.patient_name = patient_name
        self.expected_date = expected_date

    def is_valid(self):
        if isinstance(self.data, dict):
            name = u"病程记录"
            msg = u"{} 预计 {} 写的 {} 格式不对: {}".format(
                self.patient_name, self.expected_date, name, self.data )
            print(msg)
            return False

        return True

    def update(self):
        """make data correct and clean."""

        # fix and clean data
        self.json_obj['data'] = ''

        self.json_obj[KEY_FIX_INFO] = 'fix by NDIP checker'

        # add identification if null
        if KEY_ID not in self.json_obj:
            self.json_obj[KEY_ID] = str(uuid.uuid4()).replace('-', '')

        # fix status
        self.json_obj[KEY_FINISH_TAG] = False
        self.json_obj[KEY_CLASS_STATUS] = 'not-start'
