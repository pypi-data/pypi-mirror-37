import unittest
import keyword
from unittest.mock import patch
from flutils.moduleutils import (
    _expand_attr_map,
    _AttrMapping,
)


class Test(unittest.TestCase):

    def setUp(self):
        self.item = 'os.path:dirname,dname'
        self.return_value = _AttrMapping(
            'dname',
            'os.path',
            'dirname',
            self.item
        )
        patcher = patch(
            'flutils.moduleutils._expand_attr_map_item',
            return_value=self.return_value
        )
        self._expand_foreign_name = patcher.start()
        self.addCleanup(patcher.stop)

    def test_unit_expand_attr_map(self):
        val = list(_expand_attr_map((self.item, )))
        self.assertEqual(val, [self.return_value])

    def test_unit_expand_attr_map_no_duplicates(self):
        attr_map = (
            self.item,
            self.item,
        )
        val = list(_expand_attr_map(attr_map))
        self.assertEqual(val, [self.return_value])
