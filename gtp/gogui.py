import enum
from typing import Callable, Tuple

from gtp import Status, GTPRunner


class GFXType(str, enum.Enum):
    influence = 'INFLUENCE'
    label = 'LABEL'
    variation = 'VAR'
    status = 'TEXT'
    color = 'COLOR'


class GFXPlayer(str, enum.Enum):
    black = 'b'
    white = 'w'


class GFXSymbol(str, enum.Enum):
    square = 'SQUARE'
    triangle = 'TRIANGLE'
    circle = 'CIRCLE'
    mark = 'MARK'
    white = 'WHITE'
    black = 'BLACK'


class GFX:

    def __init__(self):
        self._output = {}

    def set_influence(self, vertex: str, influence: float) -> None:
        self._output[GFXType.influence] = self._output.get(GFXType.influence, '') + "{} {} ".format(vertex, influence)

    def set_color(self, vertex: str, color: str) -> None:
        key = 'COLOR {}'.format(color)
        self._output[key] = self._output.get(key, '') + "{} ".format(vertex)

    def set_label(self, vertex: str, label: str) -> None:
        self._output[GFXType.label] = self._output.get(GFXType.label, '') + "{} {} ".format(vertex, label)

    def add_variation(self, player: GFXPlayer, vertex: str) -> None:
        self._output[GFXType.variation] = self._output.get(GFXType.variation, '') + "{} {} ".format(player, vertex)

    def set_status(self, status: str) -> None:
        self._output[GFXType.status] = status

    def set_symbol(self, vertex: str, symbol: GFXSymbol) -> None:
        self._output[symbol] = self._output.get(symbol, '') + "{vertex} ".format(vertex=vertex)

    def output(self) -> str:
        return "\n".join(["{} ".format(key) + "{}".format(value).strip() for key, value in self._output.items()])


class GoGuiGTPRunner(GTPRunner):

    def __init__(self):
        super().__init__()

        self._analyze_callbacks = []

        self.add_callback('gogui_analyze_commands', self.cmd_gogui_analyze_commands, arity=0)

    def add_gfx_callback(self, name: str, callback: Callable[..., Tuple[Status, str]], arity: int, description: str=None) -> None:
        self._analyze_callbacks.append("gfx/{name}/{name}".format(name=name))
        self.add_callback(name, callback, arity, description)
        self._logger.debug("Added '%s' as GFX callback" % name)

    def cmd_gogui_analyze_commands(self, *_) -> (Status, str):
        return Status.success, "\n".join(self._analyze_callbacks)
