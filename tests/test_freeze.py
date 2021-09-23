import unittest

import hacksoc_org


class TestFreeze(unittest.TestCase):
    """ Tests for hacksoc_org.freeze and freezing functionality

    """
    def test_freeze(self):
        """Very basic test to catch runtime errors; if this fails, then there's an error somewhere!
        """
        hacksoc_org.freeze()
