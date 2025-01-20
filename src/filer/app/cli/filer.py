# -*- encoding: utf-8 -*-
"""
kara.app.commands module

Command line runner for app

"""
import multicommand
import logging
from keri import help
from filer import __version__

help.ogler.level = logging.DEBUG
help.ogler.reopen(name="reg-pilot-filer", temp=True, clear=True)

from keri.app import directing

from filer.app.cli import commands



def main():
    """ Command line process for main filer daemon """
    parser = multicommand.create_parser(commands)
    parser.add_argument('--version', action='version', version=f"%(prog)s {__version__}")
    args = parser.parse_args()

    try:
        doers = args.handler(args)
        directing.runController(doers=doers, expire=0.0)

    except Exception as ex:
        # print(f"ERR: {ex}")
        # return -1
        raise ex


if __name__ == "__main__":
    main()
