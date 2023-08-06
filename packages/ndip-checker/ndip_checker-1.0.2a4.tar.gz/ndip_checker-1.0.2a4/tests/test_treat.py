"""Test cases for Treat."""
import os
import json
import pytest
import unittest

from ndip_checker.treatment import Treat


# below are mock data file
MOCK_DATA_DIR = os.path.join('tests', 'mock_data', 'treat')
NORM_TREAT_MOCK_DATA = os.path.join(MOCK_DATA_DIR, 'norm_treat_mock.json')
DYNAMIC_TREAT_DATA = os.path.join(MOCK_DATA_DIR, 'dynamic_treat_mock.json')
NO_TAG_DATE_DATA = os.path.join(MOCK_DATA_DIR, 'no_tag_date_treat_mock.json')
DEFECT_DYNAMIC_DATA = os.path.join(MOCK_DATA_DIR, 'defect_dynamic_treat_mock.json')


class TestTreat(unittest.TestCase):
    """Test cases for Treat class."""

    def setUp(self):
        """mock some data"""

        with open(NORM_TREAT_MOCK_DATA) as data:
            mock_data = json.load(data)

        self.treat = Treat(mock_data)

    def test_dynamic_treat_check_result(self):
        """test check dynamic treat without error will return False"""

        with open(DYNAMIC_TREAT_DATA) as data:
            mock_data = json.load(data)
        treat = Treat(mock_data)
        self.assertFalse(treat.check())

    def test_no_tag_date_treat_check_result(self):
        """test check treatment without tagDate will return False, and catch output"""

        with open(NO_TAG_DATE_DATA) as data:
            mock_data = json.load(data)
        treat = Treat(mock_data)
        self.assertFalse(treat.check())

    def test_defect_dynamic_treat(self):
        """ test dynamic treatment without fix=True with defect data.
         
        will also return False, but with errors printed.
        """

        with open(DEFECT_DYNAMIC_DATA) as data:
            mock_data = json.load(data)
        treat = Treat(mock_data)
        self.assertFalse(treat.check())

    def test_check_result_is_true(self):
        """with the mock data, won't do any fix on it."""

        self.assertFalse(self.treat.check())
