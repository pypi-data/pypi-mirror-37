"""Implements ControllerApp class."""

import logging
import os
import signal
from operator import attrgetter
from .handler import make_handler
from . import exception as _exc


class ControllerApp(object):
    """Concrete class representing a controller application.

    Attributes:
        name (str): App name.
        ref (Application): Externally visible ref to this object.
        precedence (int): App precedence.
        arg_parser (ArgumentParser): Argument parser for this app.
        exception_fatal (bool|str): Terminate immediately if app raises
            exception.
        controller (Controller): App's parent controller object.
        logger (Logger): App's logger.
        handlers (Dict[str,List[BaseHandler]]): App handlers.
        bind_class (Class|None): Class for delegate instance
        bind_instance (object|None): Delegate instance
    Args:
        controller (Controller): Parent controller object.
        name (str): App name.
        ref (Application): Externally visible ref to this object.
        exception_fatal (bool): Terminate immediately if app raises exception.
        precedence (int): App precedence.
        arg_parser (ArgumentParser): Argument parser for this app.
        has_datapath_id (bool): If False, this app only handles messages
            without a datapath_id.
    """
    _curr_app_id = 0

    def __init__(self, *, controller, name, ref, exception_fatal, precedence,
                 arg_parser, has_datapath_id):
        self.name = name
        self.ref = ref
        self.precedence = precedence
        self.handlers = {}
        self.exception_fatal = exception_fatal
        self.arg_parser = arg_parser
        self._has_datapath_id = has_datapath_id
        self.bind_class = None
        self.bind_instance = None
        self.set_controller(controller)

        self.logger = logging.getLogger('%s.%s' % (__package__, self.name))
        self.logger.info('Create app "%s"', self.name)

    def set_controller(self, controller):
        """Set controller parent."""
        self.controller = controller
        # Insert app into controller's list sorted by precedence.
        controller.apps.append(self)
        controller.apps.sort(key=attrgetter('precedence'), reverse=True)

    def prepare_bind(self):
        """Construct delegate instance and bind it to handlers."""
        instance = None
        if self.bind_class:
            instance = self.bind_class()
        for item in self.handlers.values():
            for handler in item:
                handler.bind(instance)
        self.bind_instance = instance

    def handle_event(self, event, handler_type):
        """Handle event."""
        try:
            for handler in self.handlers.get(handler_type, []):
                if handler.match(event):
                    handler(event, self)
                    break
        except (_exc.StopPropagationException, _exc.PreflightUnloadException):
            # Pass this exception up to controller.
            raise
        except Exception:  # pylint: disable=broad-except
            self.handle_exception(event, handler_type)

    def handle_exception(self, event, handler_type):
        """Handle exception."""
        fatal_str = 'Fatal ' if self.exception_fatal else ''
        self.logger.critical(
            '%sException caught while handling "%s": %r',
            fatal_str,
            handler_type,
            event,
            exc_info=True)
        if self.exception_fatal:
            # If the value of `exception_fatal` is a string, find the logger
            # with this name and log the critical exception here also.
            if isinstance(self.exception_fatal, str):
                logger = logging.getLogger(self.exception_fatal)
                logger.critical(
                    '%sException caught while handling "%s": %r',
                    fatal_str,
                    handler_type,
                    event,
                    exc_info=True)
            # Shutdown the program immediately.
            logging.shutdown()
            os.kill(os.getpid(), signal.SIGKILL)

    def ensure_future(self, coroutine, *, datapath_id=None, conn_id=None):
        """Function used by an app to run an async handler.
        """
        return self.controller.ensure_future(
            coroutine, app=self, datapath_id=datapath_id, conn_id=conn_id)

    def register(self, callback, type_, subtype, options):
        """Function used to register a handler."""
        if self.controller.phase != 'INIT':
            raise RuntimeError('Controller not in INIT phase')
        if type_ == 'message' and not self._has_datapath_id and 'datapath_id' not in options:
            options['datapath_id'] = None
        handler = make_handler(callback, type_, subtype, options)
        handlers = self.handlers.setdefault(handler.type, [])
        handlers.append(handler)
        self.logger.debug('Register handler %s', handler)
        return callback
