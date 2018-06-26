import enum
from typing import Callable, Tuple

from gtp import Status, GTPRunner


class CommandType(str, enum.Enum):
    SBOARD = 'sboard'
    DBOARD = 'dboard'
    CBOARD = 'cboard'
    STRING = 'string'
    HSTRING = 'hstring'
    HPSTRING = 'hpstring'
    PSTRING = 'pstring'
    PLIST = 'plist'
    PARAM = 'param'
    PSPAIRS = 'pspairs'
    VARC = 'varc'
    GFX = 'gfx'
    NONE = 'none'


class GoGuiGTPRunner(GTPRunner):

    def __init__(self):
        super().__init__()

        self._analyze_callbacks = []

        self.add_callback('gogui_analyze_commands', self.cmd_gogui_analyze_commands, arity=0)

    def add_analyze_callback(self,
                             command_type: CommandType,
                             command_str: str,
                             callback: Callable[..., Tuple[Status, str]],
                             check_arity=True,
                             display_name: str=None,
                             description: str=None) -> None:

        command_tokens = command_str.split()

        self._assert_command_tokens(command_tokens)
        self._analyze_callbacks.append("%s/%s/%s" % (command_type.value, display_name or command_str, command_str))

        arity = len(command_tokens) - 1 if check_arity else None

        if command_tokens[0] not in self.list_commands:
            self.add_callback(command_tokens[0], callback, arity=arity, description=description)

    def cmd_gogui_analyze_commands(self, *_) -> Tuple[Status, str]:
        return Status.success, "\n".join(self._analyze_callbacks)

    @staticmethod
    def _assert_command_tokens(command_tokens) -> None:
        assert len(command_tokens) > 0

        for param in command_tokens[1:]:
            assert param in {'%s', '%p', '%c', '%w', '%r'}
