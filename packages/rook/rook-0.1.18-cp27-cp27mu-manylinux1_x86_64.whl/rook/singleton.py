"""This module is in charge of managing the rook's module state.

The external interface for the module is Rook located in rook.rook."""

import os
import six
import sys
import platform

from rook.lib.logger import logger

from rook.interfaces.config import AgentAddress

from .augs.augs_manager import AugsManager
from .output import Output
from .com.agent_com import AgentCom
from .trigger_services import TriggerServices

from rook.exceptions import RookInterfaceException, RookVersionNotSupported

class _Singleton(object):
    """This is singleton is the class managing the module.

    It should never be referred to directly, instead use obj in this module."""

    def __init__(self):
        """Initialize the object, sets member variables."""
        self._check_version_supported()

        logger.info("Initializing Rook under process-%d", os.getpid())

        self._services_started = False

        self._trigger_services = TriggerServices()
        self._output = Output(self._trigger_services)
        self._aug_manager = None

        self._agent_com = None

    def _start_trigger_services(self):
        """Start trigger services.

        Calling this method multiple times will have no effect.
        """
        # Don't double init services
        if self._services_started:
            return

        self._trigger_services.start()
        self._aug_manager = AugsManager(self._trigger_services, self._output)
        self._services_started = True

    def _stop_trigger_services(self):
        if not self._services_started:
            return

        self._aug_manager = None
        self._trigger_services.close()

        self._services_started = False

    def collect_data(self, description, send_by_default, **kwargs):
        """Collect data based on a user triggered event."""
        raise NotImplementedError()

    def connect(self, host, port, token):
        """Connect to the Agent."""
        if self._agent_com:
            raise RookInterfaceException("Multiple connection attempts not supported!")

        if not host:
            host = os.environ.get('ROOKOUT_AGENT_HOST', AgentAddress.HOST)

        if not port:
            port = int(os.environ.get('ROOKOUT_AGENT_PORT', AgentAddress.PORT))

        if not token:
            token = os.environ.get('ROOKOUT_TOKEN')

        self._start_trigger_services()

        logger.debug("Initiating AgentCom-\t%s:%d", host, port)
        self._agent_com = AgentCom(self._aug_manager, self._trigger_services, self._output, host, port, token)
        self._output.set_agent_com(self._agent_com)

        self._agent_com.connect_to_agent()
        logger.info("Successful connection to agent")

    def flush(self):
        self._output.flush_messages()

    @staticmethod
    def _check_version_supported():
        try:
            supported_platforms = ['pypy', 'cpython']
            supported_version = ['2.7', '3.5', '3.6', '3.7']

            current_platform = platform.python_implementation().lower()
            if current_platform not in supported_platforms:
                raise RookVersionNotSupported("Rook is not supported in this platform: " + current_platform)

            major, minor, _, _, _ = sys.version_info
            current_version = "{}.{}".format(major, minor)
            if current_version not in supported_version:
                raise RookVersionNotSupported("Rook is not supported in this python version: " + current_version)

        except Exception as e:
            import traceback
            traceback.print_exc()

            raise e


singleton_obj = _Singleton()
