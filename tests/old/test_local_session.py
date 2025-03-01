import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
__package__ = "tests"
from .context import LocalSession


class TestLocalSession(unittest.TestCase):
    def test_work_path(self):
        cwd = os.getcwd()
        wp = LocalSession({"work_path": cwd})
        self.assertTrue(os.path.abspath(cwd), wp.get_work_root())
