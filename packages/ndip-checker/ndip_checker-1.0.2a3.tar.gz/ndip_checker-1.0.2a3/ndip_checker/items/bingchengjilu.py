# encoding: utf-8
from . import BaseItem, KEY_FIX_INFO, KEY_FINISH_TAG, KEY_CLASS_STATUS


class BingChengJiLuItem(BaseItem):
    """培养检查项 """

    def is_valid(self):
        if isinstance(self.data, dict):
            name = u"病程记录"
            msg = u"{} 预计 {} 写的 {}(id: {}) 不是字符串格式: {}".format(
                self.patient_name, self.expected_date, name, self.identification, self.data)
            print(msg)
            return False

        return True

    def update(self):
        """make data correct and clean."""

        # fix and clean data
        self.json_obj['data'] = ''

        self.json_obj[KEY_FIX_INFO] = 'fix by NDIP checker'

        # fix status
        self.json_obj[KEY_FINISH_TAG] = False
        self.json_obj[KEY_CLASS_STATUS] = 'not-start'
