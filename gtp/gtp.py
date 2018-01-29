import enum

from logging import getLogger
from typing import Callable, Tuple
from typing import Dict

import sys

Status = enum.Enum('Status', 'success failure quit noop')


class GTPRunner:

    def __init__(self, *, logger=None):
        self._logger = logger or getLogger(__name__)

        self._callbacks = {}  # type: Dict[str, Callable[..., Tuple[Status, str]]]
        self._callback_description = {}  # type: Dict[str, str]

        self.add_callback('quit', self.cmd_quit)
        self.add_callback('list_commands', self.cmd_list_commands)
        self.add_callback('help', self.cmd_help)

        self.add_static_callback('protocol_version', '2')

    def add_callback(self, name: str, callback: Callable[..., Tuple[Status, str]], description: str=None) -> None:
        self._logger.debug("Add callback '%s'" % name)
        self._callbacks[name] = callback
        self._callback_description[name] = description

    def add_static_callback(self, name: str, value: str) -> None:
        self.add_callback(name, lambda *args: (Status.success, value))

    def execute_one_command(self, line: str) -> Tuple[Status, str]:
        words = line.split()
        command = words[0]
        params = words[1:]

        if command in self._callbacks:
            self._logger.debug("execute command '%s' with arguments %s" % (command, params))

            try:
                return self._callbacks[command](*params)
            except TypeError as e:
                description = "`{}`".format(self._callback_description[command] or "unavailable")

                return Status.failure, "Failure occurred ({e}). usage: {u}".format(e=e, u=description)

        return self.cmd_unknown_command(command)

    def execute(self, stdin=None, stdout=None) -> None:
        stdin = stdin or sys.stdin
        stdout = stdout or sys.stdout

        while True:
            line = stdin.readline()

            self._logger.debug("process line: '%s'" % line.rstrip())

            status, output = self.execute_one_command(line)

            if status == Status.noop:
                continue

            symbol = '?' if status == Status.failure else '='

            stdout.write("{symbol} {output}\n\n".format(symbol=symbol, output=output))
            stdout.flush()

            if status == Status.quit:
                break

    def cmd_list_commands(self, *_) -> Tuple[Status, str]:
        return Status.success, "\n".join([command for command in self._callbacks.keys()])

    def cmd_known_commands(self, *_) -> Tuple[Status, str]:
        return self.cmd_list_commands(_)

    def cmd_help(self, *_) -> Tuple[Status, str]:
        return self.cmd_list_commands(_)

    @staticmethod
    def cmd_quit(*_) -> Tuple[Status, str]:
        return Status.quit, "bye"

    @staticmethod
    def cmd_unknown_command(command) -> Tuple[Status, str]:
        return Status.failure, "unknown command: %s" % command
