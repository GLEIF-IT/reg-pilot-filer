# -*- encoding: utf-8 -*-
"""
filer.app.cli.commands.server module

Reg-Pilot-Filer service main command line handler.  Starts service using the provided parameters

"""
import argparse
import os
import re

import falcon
from hio.core import http
from keri import help
from keri.app import keeping, configing, habbing, oobiing
from keri.app.cli.common import existing
from keri.vdr import viring
import logging
from filer.core import basing, reporting
from filer.core.resolve_env import FilerEnvironment

parser = argparse.ArgumentParser(description='Launch vLEI Verification Service')
parser.set_defaults(handler=lambda args: launch(args),
                    transferable=True)
parser.add_argument('-p', '--http',
                    action='store',
                    default=7878,
                    help="Port on which to listen for verification requests")
parser.add_argument('-n', '--name',
                    action='store',
                    default="fdb",
                    help="Name of controller. Default is fdb.")
parser.add_argument('--base', '-b', help='additional optional prefix to file location of KERI keystore',
                    required=False, default="")
parser.add_argument('--passcode', help='22 character encryption passcode for keystore (is not saved)',
                    dest="bran", default=None)  # passcode => bran
parser.add_argument("--config-dir",
                    "-c",
                    dest="configDir",
                    help="directory override for configuration data",
                    default=None)
parser.add_argument('--config-file',
                    dest="configFile",
                    action='store',
                    default="dkr",
                    help="configuration filename override")


def launch(args):
    """ Launch the reg-pilot-filer service.

    Parameters:
        args (Namespace): command line namespace object containing the parsed command line arguments
    Returns:

    """

    name = args.name
    base = args.base
    httpPort = args.http

    configFile = args.configFile
    configDir = args.configDir

    ks = keeping.Keeper(name=name,
                        base=base,
                        temp=False,
                        reopen=True)

    aeid = ks.gbls.get('aeid')

    cf = configing.Configer(name=configFile,
                            base=base,
                            headDirPath=configDir,
                            temp=False,
                            reopen=True,
                            clear=False)

    help.ogler.level = logging.DEBUG
    filer_mode = os.environ.get("FILER_ENV", "production")
    verifier_base_url = os.environ.get("VLEI_VERIFIER", "http://localhost:7676")

    ve_init_params = {
        "configuration": cf,
        "mode": filer_mode,
        "verifier_base_url": verifier_base_url
    }


    ve = FilerEnvironment.initialize(**ve_init_params)

    fdb = basing.FilerBaser()
    cors_middleware = falcon.CORSMiddleware(
        allow_origins='*',
        allow_credentials='*',
        expose_headers=['cesr-attachment', 'cesr-date', 'content-type']
    )


    app = falcon.App(
        middleware=[cors_middleware,])

    server = http.Server(port=httpPort, app=app)
    httpServerDoer = http.ServerDoer(server=server)

    reportDoers = reporting.setup(app=app, fdb=fdb)

    doers = reportDoers + [httpServerDoer]

    print(f"Reg-Pilot-Filer Service running and listening on: {httpPort}")
    return doers