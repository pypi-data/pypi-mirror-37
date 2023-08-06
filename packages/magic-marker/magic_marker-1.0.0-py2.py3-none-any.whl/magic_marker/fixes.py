# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import absolute_import
import uuid


class Fixes(object):
    """A class containing fixes"""

    @classmethod
    def uuid(cls, mark_name):
        """The fix for a mark with a UUID

        Args:
            mark_name (str): the name of the mark to add

        Returns:
            str: the complete pytest mark to be added
        """
        return "@pytest.mark.{}('{}')\n".format(mark_name, str(uuid.uuid1()))

    @classmethod
    def empty_value(cls, mark_name):
        """The fix for a mark with a empty_value

        Args:
            mark_name (str): the name of the mark to add

        Returns:
            str: the complete pytest mark to be added
        """
        return "@pytest.mark.{}()\n".format(mark_name)
