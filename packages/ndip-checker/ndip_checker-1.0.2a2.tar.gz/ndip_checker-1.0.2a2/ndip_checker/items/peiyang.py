# encoding: utf-8
from . import BaseItem, KEY_FIX_INFO, KEY_FINISH_TAG, KEY_CLASS_STATUS


class PeiYangItem(BaseItem):
    """培养检查项 """

    items = ['date1', 'date2', 'pyResult', 'method', 'origin', 'pyChecked']

    def is_valid(self):
        name = u"培养"
        if not isinstance(self.data, dict):
            msg = u"{} 预计 {} 写的 {}(id: {}) 不是字典格式: {}".format(
                self.patient_name, self.expected_date, name,self.identification, self.data )
            print(msg)
            return False

        return True

    def update(self):
        """correct and clean data."""

        # fix and clean data
        self.json_obj['data'] = {}
        for item in PeiYangItem.items:
            self.json_obj['data'][item] = ''

        self.json_obj[KEY_FIX_INFO] = 'fix by NDIP checker'

        # fix status
        self.json_obj[KEY_FINISH_TAG] = False
        self.json_obj[KEY_CLASS_STATUS] = 'not-start'
        self.data = {}
        for item in PeiYangItem.items:
            self.data[item] = ''
