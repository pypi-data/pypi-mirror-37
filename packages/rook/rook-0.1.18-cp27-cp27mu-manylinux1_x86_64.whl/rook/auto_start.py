"""This module initializes the Rook using default settings when imported."""

import os
import six


def _auto_start():
    try:
        disable = os.environ.get('ROOKOUT_DISABLE_AUTOSTART', None)

        if disable is not None and disable != '0':
            return

        from rook.interface import Rook
        from rook.exceptions import RookCommunicationException

        obj = Rook()
        obj.start()
    except RookCommunicationException:
        six.print_("Rook failed to connect to the agent - will continue attempting in the background.")
        import traceback
        traceback.print_exc()
    except ImportError as e:
        six.print_("Rook failed to import dependencies: " + str(e))
    except BaseException:
        six.print_("Rook failed automatic initialization")
        import traceback
        traceback.print_exc()


try:
    _auto_start()
except Exception:
    pass
