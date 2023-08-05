# encoding: utf-8
from . import BaseItem
from . import KEY_FINISH_TAG, KEY_CLASS_STATUS, KEY_FIX_INFO


class TuPianItem(BaseItem):
    """培养检查项 """

    items = ['date', 'result', 'quantity', 'method', 'origin', 'tpChecked']

    def is_valid(self):
        name = u"涂片"
        if not isinstance(self.data, dict):
            msg = u"{} 预计 {} 写的 {}(id: {}) 不是字典格式: {}".format(
                self.patient_name, self.expected_date, name, self.identification, self.data)
            print(msg)
            return False

        return True

    def update(self):
        """make data correct and clean."""

        # fix and clean data
        self.json_obj['data'] = {}
        for item in TuPianItem.items:
            self.json_obj['data'][item] = ''

        self.json_obj[KEY_FIX_INFO] = 'fix by NDIP checker'

        # fix status
        self.json_obj[KEY_FINISH_TAG] = False
        self.json_obj[KEY_CLASS_STATUS] = 'not-start'
