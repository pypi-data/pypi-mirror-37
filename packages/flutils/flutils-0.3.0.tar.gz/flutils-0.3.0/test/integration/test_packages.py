import unittest
from flutils.packages import bump_version


class TestBumpVersion(unittest.TestCase):

    MSG = (
        "\n\n"
        "flutils.setuputils.bump_version({0!r}, position={1!r}, "
        "pre_release={2!r})\n"
        "       Got: {4!r}\n"
        "  Expected: {3!r}\n"
    )

    def test_bump_version__1_component_bump(self):
        with self.assertRaises(ValueError):
            bump_version('1')

    def test_bump_version__position_value(self):
        with self.assertRaises(ValueError):
            bump_version('1.2.5', position=-7)

        with self.assertRaises(ValueError):
            bump_version('1.2.5', position=3)

    def test_bump_version__2_component_position_0_bump(self):
        hold = (
            ['1.1', 0, None, '2.0'],
            ['2.3a1', 0, None, '3.0'],
            ['2.3b1', 0, None, '3.0']
        )
        for row in hold:
            row.append(bump_version(*row[0:3]))
            self.assertEqual(row[4], row[3], msg=self.MSG.format(*row))

    def test_bump_version__2_component_position_0_alpha_bump(self):

        hold = (
            ['2.3', 0, 'a', '3.0a0'],
            ['2.3a1', 0, 'alpha', '3.0a0'],
            ['2.3b1', 0, 'alpha', '3.0a0']
        )
        for row in hold:
            row.append(bump_version(*row[0:3]))
            self.assertEqual(row[4], row[3], msg=self.MSG.format(*row))

    def test_bump_version__2_component_position_0_beta_bump(self):

        hold = (
            ['4.1', 0, 'b', '5.0b0'],
            ['4.1a5', 0, 'beta', '5.0b0'],
            ['4.1b5', -2, 'beta', '5.0b0']
        )
        for row in hold:
            row.append(bump_version(*row[0:3]))
            self.assertEqual(row[4], row[3], msg=self.MSG.format(*row))

    def test_bump_version__2_component_position_1_bump(self):
        hold = (
            ['1.1', -1, None, '1.2'],
            ['1.1', 1, None, '1.2'],
            ['1.1a0', 1, None, '1.1'],
            ['1.1b0', 1, None, '1.1'],
        )
        for row in hold:
            row.append(bump_version(*row[0:3]))
            self.assertEqual(row[4], row[3], msg=self.MSG.format(*row))

    def test_bump_version__2_component_position_e_alpha_bump(self):
        hold = (
            ['1.1', -1, 'a', '1.2a0'],
            ['1.2a0', 1, 'a', '1.2a1'],
            ['1.2b1', 1, 'a', '1.3a0'],
        )
        for row in hold:
            row.append(bump_version(*row[0:3]))
            self.assertEqual(row[4], row[3], msg=self.MSG.format(*row))

    def test_bump_version__2_component_position_1_beta_bump(self):
        hold = (
            ['1.1', -1, 'b', '1.2b0'],
            ['1.1a0', 1, 'b', '1.2b0'],
            ['1.1b0', 1, 'b', '1.1b1'],
        )
        for row in hold:
            row.append(bump_version(*row[0:3]))
            self.assertEqual(row[4], row[3], msg=self.MSG.format(*row))

    def test_bump_version__3_component_position_0_bump(self):
        hold = (
            ['1.1.1', 0, None, '2.0.0'],
            ['2.1.3a1', -3, None, '3.0.0'],
            ['2.1.3b1', 0, None, '3.0.0'],

        )
        for row in hold:
            row.append(bump_version(*row[0:3]))
            self.assertEqual(row[4], row[3], msg=self.MSG.format(*row))

    def test_bump_version__3_component_position_0_alpha_bump(self):
        hold = (
            ['1.1.1', 0, 'a', '2.0.0a0'],
            ['2.1.3a1', 0, 'a', '3.0.0a0'],
            ['2.1.3b1', 0, 'a', '3.0.0a0'],
        )
        for row in hold:
            row.append(bump_version(*row[0:3]))
            self.assertEqual(row[4], row[3], msg=self.MSG.format(*row))

    def test_bump_version__3_component_position_0_beta_bump(self):
        hold = (
            ['1.1.1', 0, 'b', '2.0.0b0'],
            ['2.1.3a1', 0, 'b', '3.0.0b0'],
            ['2.1.3b1', 0, 'b', '3.0.0b0'],
        )
        for row in hold:
            row.append(bump_version(*row[0:3]))
            self.assertEqual(row[4], row[3], msg=self.MSG.format(*row))

    def test_bump_version__3_component_position_1_bump(self):
        hold = (
            ['1.1.1', 1, None, '1.2.0'],
            ['2.1.3a1', -2, None, '2.2.0'],
            ['2.5.3b1', 1, None, '2.6.0'],

        )
        for row in hold:
            row.append(bump_version(*row[0:3]))
            self.assertEqual(row[4], row[3], msg=self.MSG.format(*row))

    def test_bump_version__3_component_position_1_alpha_bump(self):
        hold = (
            ['1.1.1', 1, 'a', '1.2.0a0'],
            ['2.1.3a1', 1, 'a', '2.2.0a0'],
            ['2.5.3b1', 1, 'a', '2.6.0a0'],
        )
        for row in hold:
            row.append(bump_version(*row[0:3]))
            self.assertEqual(row[4], row[3], msg=self.MSG.format(*row))

    def test_bump_version__3_component_position_1_beta_bump(self):
        hold = (
            ['1.1.1', 1, 'b', '1.2.0b0'],
            ['2.1.3a1', 1, 'b', '2.2.0b0'],
            ['2.5.3b1', 1, 'b', '2.6.0b0'],
        )
        for row in hold:
            row.append(bump_version(*row[0:3]))
            self.assertEqual(row[4], row[3], msg=self.MSG.format(*row))

    def test_bump_version__3_component_position_2_bump(self):
        hold = (
            ['1.1.1', -1, None, '1.1.2'],
            ['2.1.3a1', 2, None, '2.1.3'],
            ['2.5.3b1', 2, None, '2.5.3'],
        )
        for row in hold:
            row.append(bump_version(*row[0:3]))
            self.assertEqual(row[4], row[3], msg=self.MSG.format(*row))

    def test_bump_version__3_component_position_2_alpha_bump(self):
        hold = (
            ['1.1.1', -1, 'a', '1.1.2a0'],
            ['2.1.3a1', 2, 'a', '2.1.3a2'],
            ['2.5.3b1', 2, 'a', '2.5.4a0'],
        )
        for row in hold:
            row.append(bump_version(*row[0:3]))
            self.assertEqual(row[4], row[3], msg=self.MSG.format(*row))

    def test_bump_version__3_component_position_2_beta_bump(self):
        hold = (
            ['1.1.1', -1, 'b', '1.1.2b0'],
            ['2.1.3a1', 2, 'b', '2.1.4b0'],
            ['2.5.3b1', 2, 'b', '2.5.3b2'],
        )
        for row in hold:
            row.append(bump_version(*row[0:3]))
            self.assertEqual(row[4], row[3], msg=self.MSG.format(*row))


