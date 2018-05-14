import io
import unittest

from gtp import GTPRunner, GTPRuntimeError, Status


class TestGTPRunner(unittest.TestCase):

    def setUp(self):
        def f_0():
            return Status.success, ""

        def f_1(_):
            return Status.success, ""

        def runtime_error():
            raise GTPRuntimeError

        self.gtp_runner = GTPRunner()

        self.gtp_runner.add_callback('arity_0', f_0, arity=0)
        self.gtp_runner.add_callback('arity_1', f_1, arity=1)
        self.gtp_runner.add_callback('runtime_error', runtime_error, arity=0)

    def test_init(self):
        self.assertIn('quit', self.gtp_runner._callbacks)
        self.assertIn('list_commands', self.gtp_runner._callbacks)
        self.assertIn('help', self.gtp_runner._callbacks)
        self.assertIn('protocol_version', self.gtp_runner._callbacks)

    def test_quit(self):
        self.assertEqual((Status.quit, 'bye'), self.gtp_runner.execute_one_command('quit'))

    def test_protocol_version(self):
        self.assertEqual((Status.success, '2'), self.gtp_runner.execute_one_command('protocol_version'))

    def test_execute(self):
        input_stream = io.StringIO("protocol_version\nquit")
        output_stream = io.StringIO()

        self.gtp_runner.execute(input_stream, output_stream)

    def test_execute_one_command_when_line_is_empty(self):
        self.assertEqual((Status.noop, ""), self.gtp_runner.execute_one_command(""))
        self.assertEqual((Status.noop, ""), self.gtp_runner.execute_one_command(" "))
        self.assertEqual((Status.noop, ""), self.gtp_runner.execute_one_command("\n"))

    def test_execute_one_command_when_arity_is_wrong(self):
        self.assertEqual(Status.failure, self.gtp_runner.execute_one_command("arity_0 x")[0])
        self.assertEqual(Status.failure, self.gtp_runner.execute_one_command("arity_1")[0])
        self.assertEqual(Status.failure, self.gtp_runner.execute_one_command("arity_1 ")[0])

    def test_execute_one_command_when_callback_raises_an_exception(self):
        self.assertEqual(Status.failure, self.gtp_runner.execute_one_command("runtime_error")[0])
