import unittest

from hacksoc_org import ROOT_DIR
import hacksoc_org.cli
import os
from shutil import rmtree

BUILD_DIR = os.path.join(ROOT_DIR, "build")


class TestFreeze(unittest.TestCase):
    """Tests for hacksoc_org.freeze and freezing functionality"""

    def setUp(self) -> None:
        try:
            rmtree(BUILD_DIR)
        except FileNotFoundError:
            pass

    def tearDown(self) -> None:
        try:
            rmtree(BUILD_DIR)
        except FileNotFoundError:
            pass

    def test_freeze(self):
        """Very basic test to catch runtime errors; if this fails, then there's an error somewhere!"""
        hacksoc_org.cli.main(args=["freeze"])

        self.assertTrue(os.path.exists(BUILD_DIR), f"Expected {BUILD_DIR} to exist")
        self.assertTrue(os.path.isdir(BUILD_DIR), f"Expected {BUILD_DIR} to be a directory")
