# encoding: utf-8
from abc import ABCMeta


class BaseItem:
    """Base check item class."""

    __metaclass__ = ABCMeta

    def __init__(self, json_obj, patient_name, expected_date):
        self.json_obj = json_obj
        self.data = json_obj['data']
        self.identification = json_obj.get('identification', u'空')
        self.patient_name = patient_name
        self.expected_date = expected_date

    def is_valid(self):
        """check whether the data is valid."""
        return True
