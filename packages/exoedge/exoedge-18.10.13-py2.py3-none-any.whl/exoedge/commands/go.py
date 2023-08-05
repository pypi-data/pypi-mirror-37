# pylint: disable=C0103,C0301,W1202
"""
Primary module to support edged tool.
"""
from __future__ import print_function
import os
import sys
import logging
import json
import time
import threading
from exoedge import logger
from exoedge.exo_edge import ExoEdge
from exoedge.commands import Command
from exoedge.constants import OPTION_NAME_MAPPER, OPTION_TYPE_MAP, OPTION_PRECEDENCE, DEFAULTS

LOG = logger.getLogger('EXOEDGE.' + __name__)

class ExoCommand(Command):
    """
    Create and start ExoSense client.

    usage:
        go [options]

    options:
        -h --help           Show this screen.
    """
    Name = 'go'

    def execute(self):
        from murano_client.client import MuranoClient
        from exoedge.options_handler import OptionsHandler


        # --------------------------------------
        # OPTIONS HANDLING
        # --------------------------------------
        # The value of an option comes from, in
        # decreasing priority:
        #   1. CLI switches
        #   2. Environment variables
        #   3. INI file
        #   4. Defaults
        # --------------------------------------
        OH_ARGS = {
            'cli': self.global_args,
            'env': os.environ,
            'dft': DEFAULTS
        }

        # -----------------------------------------
        # Include INI?
        _INI_FP = OH_ARGS['cli'].get('--ini-file') or OH_ARGS['env'].get('EDGED_INI_FILE') or None
        _NO_FS = OH_ARGS['cli'].get('--no-filesystem') or OH_ARGS['env'].get('EDGED_NO_FILESYSTEM') or None
        _INI_FILE = _INI_FP and not _NO_FS
        if _INI_FILE:
            from murano_client.atomicconfigparser import atomicconfigparser as IniParser
            I = IniParser(allow_no_value=True)
            I.read(_INI_FP)

            INI_VALUES = {}
            for s in I.sections():
                LOG.info('INI section %s...', s)
                for o, v in I.items(s):
                    LOG.info('INI option %s has value %s', o, v)
                    INI_VALUES.update({o: v})
            OH_ARGS.update({'ini': INI_VALUES})
        # -----------------------------------------


        OH = OptionsHandler(OPTION_PRECEDENCE,
                            OPTION_TYPE_MAP,
                            OPTION_NAME_MAPPER,
                            **OH_ARGS)
        PARAMETERS = OH.values
        LOG.info(json.dumps(PARAMETERS, indent=2))

        # -----------------------------------------
        # Define MuranoClient object
        # -----------------------------------------
        D = MuranoClient(**PARAMETERS)
        D.client_activate()
        TOKEN = D.murano_token() or PARAMETERS.get('murano_token') or None
        if _INI_FILE:
            if 'device' not in I.sections():
                I.add_section('device')
            I.set('device', 'murano_token', TOKEN)
            I.write(_INI_FP)
            LOG.critical('TOKEN saved to %s', _INI_FP)
        LOG.critical('TOKEN: %s', TOKEN)


        # -----------------------------------------
        # Define ExoEdge object
        # -----------------------------------------
        E = ExoEdge(D, **PARAMETERS)


        # -----------------------------------------
        # Start Reporting
        # -----------------------------------------
        E.setup()

        EDGED_TIMEOUT = self.global_args.get('--edged-timeout')
        def STOP_PROCESS():
            D.stop_all()
            E.stop()
            for thread in threading.enumerate():
                if hasattr(thread, 'stop'):
                    LOG.critical("Stopping thread: {}".format(thread))
                    if hasattr(thread, 'is_stopped'):
                        if not thread.is_stopped():
                            thread.stop()

            LOG.critical('TOKEN: %s', TOKEN)
            exit(0)

        try:
            if EDGED_TIMEOUT:
                EDGED_TIMEOUT = float(EDGED_TIMEOUT)
                BEGINNING = time.time()
                while time.time() < BEGINNING + EDGED_TIMEOUT:
                    time.sleep(1)
                STOP_PROCESS()
            else:
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            STOP_PROCESS()
        return
