import re

from typing import Optional, Tuple


_LETTERS = 'ABCDEFGHJKLMNOPQRST'  # excluding 'i'
_VALID_MOVE_PATTERN = r"[A-HJ-T][\d]{1,2}"
_MATCHER = re.compile(_VALID_MOVE_PATTERN, re.IGNORECASE)


COLOR_BLACK = 'black'
COLOR_WHITE = 'white'


def parse_color(color_str: str) -> str:
    """
    Parses a given string and returns a formatted string
    as per the result of parsing if the string is
    valid GTP string.
    If not valid, ValueError is thrown.

    :param color_str: string to be parsed
    :return: either `COLOR_BLACK` or `COLOR_WHITE`:
    :exception ValueError if `color_str` is an invalid gtp color string
    """
    if color_str.upper() == 'B':
        return COLOR_BLACK
    elif color_str.upper() == 'W':
        return COLOR_WHITE

    raise ValueError("Cannot parse string `%s`" % color_str)


def parse_move(move_str: str) -> Optional[Tuple[int, int]]:
    """
    Parses a given string and returns Tuple of int or None as per the given string.
    If the string is not valid, ValueError is thrown.
    """
    if move_str.lower() == 'pass':
        return None

    if _MATCHER.match(move_str):
        alphabet = move_str[0].upper()
        number = move_str[1:]

        row = _LETTERS.find(alphabet)
        col = int(number) - 1

        if 0 <= row < 19 and 0 <= col < 19:
            return row, col

    raise ValueError("Cannot parse string `%s`" % move_str)


def move_to_str(move) -> Optional[str]:
    """
    Returns a GTP string as per the given Move instance.
    e.g., "PASS", "A19", "J1" if the argument is None, (0, 18), (8, 0) respectively.
    """
    if move is None:
        return "PASS"

    if not isinstance(move, tuple):
        return None

    if not (0 <= move[0] < 19 and 0 <= move[1] < 19):
        return None

    row = _LETTERS[move[0]]
    col = move[1] + 1

    return "%s%s" % (row, col)


