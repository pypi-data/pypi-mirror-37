from abc import ABCMeta


class BaseItem:
    """Base check item class."""

    __metaclass__ = ABCMeta

    def is_valid(self):
        """check whether the data is valid."""
        return True
