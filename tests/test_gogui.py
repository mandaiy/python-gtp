from unittest import TestCase

from gtp import Status
from gtp.gogui import GoGuiGTPRunner, CommandType, GoGuiParam, GoGuiParams


class TestGoGuiGTPRunner(TestCase):

    def setUp(self):
        self.gtp_runner = GoGuiGTPRunner()

    def test_init(self):
        self.assertIn('gogui_analyze_commands', self.gtp_runner._callbacks)

    def test_add_analyze_command(self):
        self.gtp_runner.add_analyze_callback(CommandType.NONE, 'command', lambda *args: (Status.success, ""))

        self.assertIn('command', self.gtp_runner.list_commands)

    def test_add_analyze_command_command_str_is_invalid_then_raises_assertion_error(self):
        def f():
            return Status.success, ""

        with self.assertRaises(AssertionError):
            self.gtp_runner.add_analyze_callback(CommandType.NONE, '', f)

        with self.assertRaises(AssertionError):
            self.gtp_runner.add_analyze_callback(CommandType.NONE, 'command %a', f)


class TestGoGuiParam(TestCase):

    def test_init(self):
        params = GoGuiParams([
            GoGuiParam('param1', 'bool', 1),
            GoGuiParam('param2', 'string', 'foo')
        ])

        expected_str = '[bool] param1 1\n[string] param2 foo'

        self.assertIn('param1', params.param_names)
        self.assertIn('param2', params.param_names)

        self.assertEqual(1, params.param1)
        self.assertEqual('foo', params.param2)

        self.assertEqual(expected_str, str(params))
        self.assertEqual((Status.success, expected_str), params())

    def test_update(self):
        params = GoGuiParams([
            GoGuiParam('param', 'bool', 0)
        ])

        self.assertEqual(0, params.param)

        params('param', 1)

        expected_str = '[bool] param 1'

        self.assertEqual(1, params.param)
        self.assertEqual(expected_str, str(params))
        self.assertEqual((Status.success, expected_str), params())
