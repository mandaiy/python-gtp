from unittest import TestCase

from gtp import Status
from gtp.gogui import GoGuiGTPRunner, CommandType


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
