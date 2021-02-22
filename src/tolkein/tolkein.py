#!/usr/bin/env python3
"""
Tolkein.

usage: tolkein [<command>] [<args>...] [-h|--help] [--version]

commands:
    -h, --help      show this
    -v, --version   show version number
"""

import sys

from docopt import DocoptExit
from docopt import docopt
from pkg_resources import working_set

from .lib.tolog import logger
from .lib.version import __version__

LOGGER = logger(__name__)


def cli():
    """Entry point."""
    if len(sys.argv) > 1:
        try:
            args = docopt(__doc__, help=False, version=__version__)
        except DocoptExit:
            args = {"<command>": sys.argv[1]}
        if args["<command>"]:
            # load <command> from entry_points
            for entry_point in working_set.iter_entry_points("tolkein.subcmd"):
                if entry_point.name == args["<command>"]:
                    subcommand = entry_point.load(sys.argv[1:])
                    sys.exit(subcommand())
            LOGGER.error("'tolkein %s' is not a valid command", args["<command>"])
            sys.exit(1)
    print(__doc__)
    raise DocoptExit
