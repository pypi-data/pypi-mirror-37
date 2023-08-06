import unittest
from flutils.setuputils import _SetupCfg

CONFIG = """
[test]
foo = bar
"""


class TestSetupCfg(unittest.TestCase):

    def setUp(self):
        self.skipTest('')

    def test_integration_does_not_exist(self):
        cfg = _SetupCfg()
        with self.assertRaises(SystemExit):
            cfg.load('')

    def test_integration_missing_section(self):
        cfg = _SetupCfg()
        cfg.cfg.read_string(CONFIG)
        with self.assertRaises(SystemExit):
            cfg.get('tests', 'a')

    def test_integration_missing_section_default(self):
        cfg = _SetupCfg()
        cfg.cfg.read_string(CONFIG)
        data = cfg.get('tests', 'a', default='foo')
        self.assertEqual(data, 'foo')

    def test_integration_missing_option(self):
        cfg = _SetupCfg()
        cfg.cfg.read_string(CONFIG)
        with self.assertRaises(SystemExit):
            cfg.get('test', 'a')

    def test_integration_missing_option_default(self):
        cfg = _SetupCfg()
        cfg.cfg.read_string(CONFIG)
        data = cfg.get('test', 'a', default='foo')
        self.assertEqual(data, 'foo')


