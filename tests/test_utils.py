import unittest

from gtp.utils import parse_color, parse_move, move_to_str, COLOR_BLACK, COLOR_WHITE


class TestGtpUtils(unittest.TestCase):

    def test_parse_color_when_argument_is_valid_then_returns_color(self):
        self.assertEqual(COLOR_BLACK, parse_color('b'))
        self.assertEqual(COLOR_BLACK, parse_color('B'))

        self.assertEqual(COLOR_WHITE, parse_color('w'))
        self.assertEqual(COLOR_WHITE, parse_color('W'))

    def test_parse_color_when_argument_is_invalid_then_returns_none(self):
        self.assertRaises(ValueError, parse_color, 'invalid')

        self.assertRaises(ValueError, parse_color, 'bAAAAAA')
        self.assertRaises(ValueError, parse_color, 'BAAAAAA')

        self.assertRaises(ValueError, parse_color, 'wAAAAAA')
        self.assertRaises(ValueError, parse_color, 'WAAAAAA')

    def test_parse_move_when_argument_is_valid_then_returns_move(self):
        self.assertEqual((0, 0), parse_move('a1'))
        self.assertEqual((0, 0), parse_move('A1'))
        self.assertEqual((18, 18), parse_move('t19'))
        self.assertEqual((18, 18), parse_move('T19'))

        self.assertEqual(None, parse_move('pass'))
        self.assertEqual(None, parse_move('PASS'))

    def test_parse_move_when_argument_is_invalid_then_returns_none(self):
        self.assertRaises(ValueError, parse_move, 'A20')
        self.assertRaises(ValueError, parse_move, 'U1')

        self.assertRaises(ValueError, parse_move, 'A 1')
        self.assertRaises(ValueError, parse_move, 'invalid text')

    def test_move_to_str_when_argument_is_valid_then_returns_str(self):
        self.assertEqual('A1', move_to_str((0, 0)))
        self.assertEqual('T19', move_to_str((18, 18)))

        self.assertEqual('PASS', move_to_str(None))

    def test_move_to_str_when_argument_is_invalid_then_returns_none(self):
        self.assertIsNone(move_to_str((-1, -1)))
        self.assertIsNone(move_to_str((19, 19)))

        self.assertIsNone(move_to_str([0, 0]))
