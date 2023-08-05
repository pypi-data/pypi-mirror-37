# -*- coding: utf-8 -*-
import logging
import sys
import traceback


logging.basicConfig()

dtslogger = logging.getLogger('dts')
dtslogger.setLevel(logging.DEBUG)

__version__ = '3.0.13'

dtslogger.info('duckietown-shell %s' % __version__)

import termcolor


from .cli import DTShell

from .dt_command_abs import DTCommandAbs
from .dt_command_placeholder import DTCommandPlaceholder


if sys.version_info >= (3,):
    msg = "duckietown-shell only works on Python 2.7. Python 3 is not supported yet."
    dtslogger.warning(msg)
    # raise ImportError(msg)


def cli_main():
    from .col_logging import setup_logging_color
    setup_logging_color()
    # TODO: register handler for Ctrl-C
    msg = """

        Problems with a step in the Duckiebot operation manual?

            Report here: https://github.com/duckietown/docs-opmanual_duckiebot/issues


        Other problems?  

            Report here: https://github.com/duckietown/duckietown-shell-commands/issues

            Tips:

            - NEVER install duckietown-shell using "sudo". Instead use:

                pip install --user -U duckietown-shell

              Note the switch "--user" to install in ~/.local

            - Delete ~/.dt-shell to reset the shell to "factory settings".
              This is useful if some update fails.

              (Note: you will have to re-configure)

            - Last resort is deleting ~/.local and re-install from scratch.

    """
    dtslogger.info(msg)

    from .env_checks import InvalidEnvironment

    shell = DTShell()
    arguments = sys.argv[1:]

    known_exceptions = (InvalidEnvironment,)

    try:
        if arguments:
            from dt_shell.utils import replace_spaces
            arguments = map(replace_spaces, arguments)
            cmdline = " ".join(arguments)
            shell.onecmd(cmdline)
        else:
            shell.cmdloop()
    except known_exceptions as e:
        msg = str(e)
        termcolor.cprint(msg, 'yellow')
        sys.exit(1)
    except Exception as e:
        msg = traceback.format_exc(e)
        termcolor.cprint(msg, 'red')
        sys.exit(2)

