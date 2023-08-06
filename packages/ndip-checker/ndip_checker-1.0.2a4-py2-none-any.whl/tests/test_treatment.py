import pytest
from unittest import TestCase

from ndip_checker.treatment import Treatment


class TreatmentTest(TestCase):
    """Test case for Treatment"""

    def setUp(self):
        mock_data = {'a': 1}
        self.treatment = Treatment(mock_data, 1, 1)
