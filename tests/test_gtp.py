import io
import unittest

from gtp.gtp import *


class TestGtp(unittest.TestCase):

    def setUp(self):
        self.gtp_runner = GTPRunner()

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
