#!/usr/bin/env python

from logging import getLogger, basicConfig, INFO

from gtp.gogui import GoGuiGTPRunner, CommandType

from gtp import Status


logger = getLogger(__name__)
basicConfig(format="%(levelname)s %(message)s", level=INFO)


def any_callback(*args):
    for arg in args:
        logger.info("%s" % arg)
    return Status.success, ""


if __name__ == '__main__':
    gtp_runner = GoGuiGTPRunner()

    gtp_runner.add_static_callback('name', 'dummy')
    gtp_runner.add_static_callback('version', '0.0.0')
    gtp_runner.add_callback('boardsize', any_callback, arity=1)
    gtp_runner.add_callback('clear_board', any_callback, arity=0)
    gtp_runner.add_callback('komi', any_callback, arity=1)
    gtp_runner.add_callback('play', any_callback, arity=2)

    gtp_runner.add_analyze_callback(CommandType.GFX, 'test %p %c', any_callback)

    gtp_runner.execute()
