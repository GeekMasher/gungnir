
import platform
import unittest

from gungnir.project import OperatingSystem


class TestProjects(unittest.TestCase):
    def test_os(self):
        os = OperatingSystem("testing")
        # defaults
        self.assertEqual(os.version, platform.release())


